import logging

from jobfit.model.error_summary import ErrorCount, LogInsightsOutput

from .query import LogsInsightsClient


class FetchingClient:
    def __init__(self, client: LogsInsightsClient):
        self._client = client

    def fetch_error_pattern(
        self, log_groups: list[str], start_time: int, end_time: int
    ) -> list[LogInsightsOutput]:
        """Fetch error-level patterns excluding silent errors."""
        logging.info(f"Fetching error-level patterns for {log_groups}")

        query_string = """filter level = "ERROR" 
        | filter (not ispresent(extra.silent) or extra.silent = 0) 
        | fields concat(@log, " ", @message) as logGroupMessage 
        | pattern logGroupMessage"""
        try:
            logs = self._client.query(log_groups, start_time, end_time, query_string)
        except Exception:
            raise

        return [LogInsightsOutput.from_insights_result(log) for log in logs]

    def fetch_http_errors(
        self, log_groups: list[str], start_time: int, end_time: int
    ) -> list[ErrorCount]:
        """Fetch HTTP errors."""
        logging.info(f"Fetching HTTP errors for {log_groups}")

        query_string = """stats sum(http.status = 400) as `HTTP 400`,
            sum(http.status = 401) as `HTTP 401`,
            sum(http.status = 403) as `HTTP 403`,
            sum(http.status = 404) as `HTTP 404`,
            sum(http.status = 405) as `HTTP 405`,
            sum(http.status = 409) as `HTTP 409`,
            sum(http.status = 500) as `HTTP 500`,
            sum(http.status >= 406 and http.status != 409 and http.status != 500) as Unexpected"""
        try:
            results = self._client.query(log_groups, start_time, end_time, query_string)
        except Exception:
            raise

        return [ErrorCount.model_validate(result) for result in results[0]]
