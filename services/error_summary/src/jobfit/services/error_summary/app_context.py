import logging
from functools import cached_property
from typing import Self, override

from jobfit.app import ServiceContext
from jobfit.app.logging import LambdaJsonFormatter, setup_logger
from jobfit.llm.openai import GptClient
from jobfit.observability import install_tracing

from .config import AppConfig
from .fetch import FetchingClient
from .query import LogsInsightsClient


class AppContext(ServiceContext[AppConfig]):
    @override
    def install(self) -> Self:
        setup_logger(
            formatter=LambdaJsonFormatter(),
            level=logging.getLevelName(self.config.service_log_level.value),
        )

        if self.config.tracing:
            install_tracing()

        return self

    # Note: no def uninstall(self), because there's no good way to invoke it on AWS Lambda.

    @cached_property
    def openai_client(self) -> GptClient:
        return GptClient(self.config.llm.get_default(self.config.openai_api_key))

    @cached_property
    def logs_insights_client(self) -> LogsInsightsClient:
        return LogsInsightsClient(
            self.config.query_polling_attempts, self.config.query_polling_interval
        )

    @cached_property
    def fetching_client(self) -> FetchingClient:
        return FetchingClient(self.logs_insights_client)
