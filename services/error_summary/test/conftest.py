import pytest
from pydantic import HttpUrl

from jobfit.llm import LlmEndpointConfig, LlmEndpointsConfig
from jobfit.services.error_summary.app_context import AppContext
from jobfit.services.error_summary.config import AppConfig


@pytest.fixture
def config() -> AppConfig:
    return AppConfig(
        openai_api_key="mock-openai-api-key",
        llm=LlmEndpointsConfig(
            endpoints={
                "gpt-4.1-mini": LlmEndpointConfig(url=HttpUrl("https://example.org")),
            },
            default="gpt-4.1-mini",
        ),
        log_groups=["mock-log-group"],
        sns_topic_arn="mock-sns-topic-arn",
    )


@pytest.fixture
def context(config):
    """Mock the AppContext with test configuration."""
    context = AppContext(config)
    return context
