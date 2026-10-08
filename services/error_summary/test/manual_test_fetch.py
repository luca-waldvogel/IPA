from jobfit.services.error_summary.fetch import FetchingClient
from jobfit.services.error_summary.formatter import format_log_insights_output
from jobfit.services.error_summary.query import LogsInsightsClient

LOG_CLIENT = LogsInsightsClient(5, 6)
CLIENT = FetchingClient(LOG_CLIENT)
LOG_GROUPS = [
    "/aws/lambda/jobfit-ingestion-prod",
    "/aws/lambda/jobfit-extraction-prod",
    "/aws/lambda/jobfit-elaboration-prod",
    "/ecs/jobfit-api-prod",
    "/aws/lambda/jobfit-pipe-enricher-prod",
    "/aws/lambda/jobfit-pool-ingestion-prod",
    "/ecs/jobfit-pool-api-prod",
    "/ecs/jobfit-migrator-prod",
]
API_LOG_GROUPS = ["/ecs/jobfit-api-prod", "/ecs/jobfit-pool-api-prod"]


def main():
    """
    This test is meant to be run manually to check the output of the fetch_error_pattern and fetch_http_errors methods with real
    CloudWatch Logs data. It doesn't have any assertions, but it prints the output in a readable format for manual inspection.

    Command (from the jobfit/services/error_summary directory):
    `aws-vault exec snm-prod-write -- uv run python test/manual_test_fetch.py`
    """
    output = CLIENT.fetch_error_pattern(
        LOG_GROUPS,
        1773844143,
        1773930543,
    )
    http = CLIENT.fetch_http_errors(API_LOG_GROUPS, 1773844143, 1773930543)
    formatted = format_log_insights_output(output, LOG_GROUPS)

    for i, log in enumerate(formatted):
        print(f"""-------PATTERN {i}-------
Pattern:
{log.pattern}
Log Group:
{log.log_groups}
Log Sample:
{log.log_sample}
Sample Count:
{log.sample_count}""")

    print("-------HTTP ERRORS-------")
    print(http)


if __name__ == "__main__":
    main()
