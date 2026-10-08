import json
from unittest.mock import Mock

import pytest

from jobfit.model.error_summary import ErrorCount
from jobfit.services.error_summary.main import ErrorSummaryResponse, handle
from jobfit.services.error_summary.program import ErrorSummaryProgram

SNS_TOPIC_ARN = "mock-sns-topic-arn"
SUMMARY_TEXT = "Error Summary"


@pytest.fixture
def mock_fetching_client():
    client = Mock()
    client.fetch_error_pattern.return_value = []
    client.fetch_http_errors.return_value = [
        ErrorCount(field="HTTP 400", value=0),
        ErrorCount(field="HTTP 500", value=3),
    ]
    return client


@pytest.fixture
def mock_program_run(mocker):
    output = Mock()
    output.result = SUMMARY_TEXT
    return mocker.patch.object(ErrorSummaryProgram, "run", return_value=output)


@pytest.fixture
def mock_sns_client(mocker):
    sns = Mock()
    sns.publish.return_value = {"MessageId": "test-message-id"}
    mocker.patch("boto3.client", return_value=sns)
    return sns


def _activate_context(context, mock_fetching_client):
    """Inject the mock fetching client into the context's cached_property slot."""
    context.__dict__["fetching_client"] = mock_fetching_client
    return context


def test_handle_publishes_to_sns(
    context, mock_fetching_client, mock_program_run, mock_sns_client
):
    with _activate_context(context, mock_fetching_client):
        result = handle({})

    assert isinstance(result, ErrorSummaryResponse)
    mock_sns_client.publish.assert_called_once()

    call_kwargs = mock_sns_client.publish.call_args.kwargs
    assert call_kwargs["TopicArn"] == SNS_TOPIC_ARN

    message = json.loads(call_kwargs["Message"])
    assert message["source"] == "custom"
    assert message["content"]["textType"] == "client-markdown"
    assert "24 hours" in message["content"]["title"]
    assert message["content"]["description"] == SUMMARY_TEXT


def test_handle_monday_uses_weekend_title(
    context, mock_fetching_client, mock_program_run, mock_sns_client
):
    with _activate_context(context, mock_fetching_client):
        result = handle({"is_monday": True})

    assert isinstance(result, ErrorSummaryResponse)

    call_kwargs = mock_sns_client.publish.call_args.kwargs
    assert call_kwargs["TopicArn"] == SNS_TOPIC_ARN

    message = json.loads(call_kwargs["Message"])
    assert "weekend" in message["content"]["title"].lower()
    assert message["content"]["description"] == SUMMARY_TEXT
