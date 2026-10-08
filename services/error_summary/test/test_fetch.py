from unittest.mock import MagicMock

import pytest

from jobfit.model.error_summary import ErrorCount, LogInsightsOutput
from jobfit.services.error_summary.fetch import FetchingClient
from jobfit.services.error_summary.query import QueryError

LOG_GROUPS = ["/ecs/my-service"]
START_TIME = 1700000000
END_TIME = 1700003600


def make_pattern_entry(
    pattern: str = "JWT has expired",
    log_samples: str = "[]",
    tokens: str = '["JWT", "expired"]',
    sample_count: int = 10,
) -> list[dict]:
    return [
        {"field": "@pattern", "value": pattern},
        {"field": "@logSamples", "value": log_samples},
        {"field": "@tokens", "value": tokens},
        {"field": "@sampleCount", "value": str(sample_count)},
    ]


@pytest.fixture()
def mock():
    return MagicMock()


def test_fetch_error_pattern_returns_parsed_outputs(mock):
    """Test that results are parsed into LogInsightsOutput objects."""

    mock.query.return_value = [make_pattern_entry()]
    result = FetchingClient(mock).fetch_error_pattern(LOG_GROUPS, START_TIME, END_TIME)

    assert len(result) == 1
    assert isinstance(result[0], LogInsightsOutput)
    assert result[0].pattern == "JWT has expired"
    assert result[0].sample_count == 10
    assert result[0].tokens == '["JWT", "expired"]'


def test_fetch_error_pattern_empty_results(mock):
    """Test that an empty query result returns an empty list."""

    mock.query.return_value = []
    result = FetchingClient(mock).fetch_error_pattern(LOG_GROUPS, START_TIME, END_TIME)

    assert result == []


def test_fetch_error_pattern_propagates_query_error(mock):
    """Test that QueryError is propagated."""

    mock.query.side_effect = QueryError("Logs insights query failed or timed out.")
    with pytest.raises(QueryError, match="Logs insights query failed or timed out."):
        FetchingClient(mock).fetch_error_pattern(LOG_GROUPS, START_TIME, END_TIME)


def test_fetch_http_errors_returns_error_counts(mock):
    mock.query.return_value = [
        [
            {"field": "HTTP 400", "value": "5"},
            {"field": "HTTP 500", "value": "2"},
        ]
    ]
    result = FetchingClient(mock).fetch_http_errors(LOG_GROUPS, START_TIME, END_TIME)

    assert len(result) == 2
    assert isinstance(result[0], ErrorCount)
    assert result[0].error == "HTTP 400"
    assert result[0].count == 5
    assert result[1].error == "HTTP 500"
    assert result[1].count == 2
