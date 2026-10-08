from unittest.mock import patch

import pytest

from jobfit.services.error_summary.query import LogsInsightsClient, QueryError

LOG_GROUPS = ["123456789012:my-service"]
START_TIME = 1700000000
END_TIME = 1700003600
QUERY_STRING = 'fields @message | filter level = "ERROR"'


@pytest.fixture()
def mock_boto_client():
    with patch("jobfit.services.error_summary.query.boto3.client") as mock:
        yield mock.return_value


@pytest.fixture()
def client():
    return LogsInsightsClient(polling_attempts=2, polling_interval=0)


def test_query_returns_results(mock_boto_client, client):
    """Successful query returns parsed results."""

    results = [[{"field": "@message", "value": "error occurred"}]]
    mock_boto_client.start_query.return_value = {"queryId": "qid-1"}
    mock_boto_client.get_query_results.return_value = {
        "results": results,
        "status": "Complete",
    }

    result = client.query(LOG_GROUPS, START_TIME, END_TIME, QUERY_STRING)

    assert result == results


def test_query_raises_after_max_attempts(mock_boto_client, client):
    """Raises QueryError when query never completes within polling_attempts."""

    mock_boto_client.start_query.return_value = {"queryId": "qid-3"}
    mock_boto_client.get_query_results.return_value = {
        "results": [],
        "status": "Running",
    }

    with pytest.raises(QueryError, match="Logs insights query failed or timed out."):
        client.query(LOG_GROUPS, START_TIME, END_TIME, QUERY_STRING)

    assert mock_boto_client.get_query_results.call_count == 2


def test_query_returns_empty_results(mock_boto_client, client):
    """Empty results from CloudWatch are returned as an empty list."""

    mock_boto_client.start_query.return_value = {"queryId": "qid-5"}
    mock_boto_client.get_query_results.return_value = {
        "results": [],
        "status": "Complete",
    }

    result = client.query(LOG_GROUPS, START_TIME, END_TIME, QUERY_STRING)

    assert result == []
