import logging
import time

import boto3

from jobfit.model.error_summary import QueryResponse, QueryResult


class QueryError(Exception):
    """Raised when a CloudWatch Logs Insights query fails or times out."""


class LogsInsightsClient:
    """Fetch Logs insights from CloudWatch Logs."""

    def __init__(self, polling_attempts: int, polling_interval: int):
        self._polling_attempts = polling_attempts
        self._polling_interval = polling_interval
        self._client = boto3.client("logs")

    def query(
        self, log_groups: list[str], start_time: int, end_time: int, query_string: str
    ) -> list[list[dict]]:
        """Query logs insights."""
        query_response = self._client.start_query(
            logGroupNames=log_groups,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
        )
        response = QueryResponse.model_validate(query_response)

        result = self._polling(response.query_id)
        return result.results

    def _polling(self, query_id: str) -> QueryResult:
        """Polling for logs insights."""
        for _ in range(self._polling_attempts):
            time.sleep(self._polling_interval)
            query_result = self._client.get_query_results(queryId=query_id)
            result = QueryResult.model_validate(query_result)

            if result.status == "Complete":
                return result

        logging.error(
            f"Logs insights query failed or timed out for query_id: {query_id}"
        )
        raise QueryError("Logs insights query failed or timed out.")
