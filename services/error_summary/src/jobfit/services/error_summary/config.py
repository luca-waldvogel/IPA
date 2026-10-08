from typing import Annotated

from jobfit.app import LoggingLevel, ServiceConfig, SsmParam
from jobfit.llm import LlmEndpointsConfig

ERROR_SUMMARY_MAX_TOKENS = 3000


class AppConfig(ServiceConfig, ssm_prefix="/jobfit-services-shared/"):
    openai_api_key: Annotated[str, SsmParam()]  # SSM or ENV: OPENAI_API_KEY
    """
    API key for the OpenAI service, shared between all the endpoints.
    """

    llm: LlmEndpointsConfig  # ENV: LLM
    """
    Configuration of the available LLM endpoints.
    """

    log_groups: list[str]  # ENV: LOG_GROUPS
    """
    List of CloudWatch log groups to create the summary for.
    """

    sns_topic_arn: str  # ENV: SNS_TOPIC_ARN
    """
    SNS topic ARN to publish the error summary to.
    """

    tracing: bool = False  # ENV: TRACING
    """
    Should tracing using AWS X-Ray be enabled?
    """

    service_log_level: LoggingLevel = LoggingLevel.INFO  # ENV: SERVICE_LOG_LEVEL
    """
    Logging level for the service.
    """

    query_polling_attempts: int = 5  # ENV: QUERY_POLLING_ATTEMPTS
    """
    Polling attempts for CloudWatch Logs insights query results.
    """

    query_polling_interval: int = 3  # ENV: QUERY_POLLING_INTERVAL
    """
    Polling interval for CloudWatch Logs insights query results.
    """

    query_retry: bool = True  # ENV: QUERY_RETRY
    """
    Should the query be retried if it fails?
    """
