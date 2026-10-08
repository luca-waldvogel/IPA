import json
import logging
from datetime import datetime
from typing import Any

import boto3
from pydantic import BaseModel

from .app_context import AppContext
from .formatter import format_log_insights_output
from .program import (
    ErrorSummaryProgram,
    ErrorSummaryRequest,
)


class ErrorSummaryResponse(BaseModel):
    pass


def handle(payload: dict[str, Any]) -> ErrorSummaryResponse:
    logging.debug(f"Processing error summary payload: {payload}")
    context = AppContext.current
    program = ErrorSummaryProgram()
    is_monday = payload.get("is_monday", False)

    request = _get_error_summary_request(context, is_monday)
    output = program.run(input=request, llm_client=context.openai_client)
    summary = output.result

    _publish_error_summary(context.config.sns_topic_arn, summary, is_monday)
    return ErrorSummaryResponse()


def _get_error_summary_request(
    context: AppContext, is_monday: bool = False
) -> ErrorSummaryRequest:
    client = context.fetching_client
    log_groups = context.config.log_groups
    end_time = int(datetime.now().timestamp())
    start_time = (end_time - 3600 * 72) if is_monday else (end_time - 3600 * 24)

    error_patterns_output = client.fetch_error_pattern(log_groups, start_time, end_time)
    error_patterns = format_log_insights_output(error_patterns_output, log_groups)
    http_errors = client.fetch_http_errors(log_groups, start_time, end_time)

    return ErrorSummaryRequest(error_patterns=error_patterns, http_errors=http_errors)


def _publish_error_summary(arn: str, summary: str, is_monday: bool = False):
    title = (
        "⚠️ Error Summary of the weekend (past 72 hours) ⚠️"
        if is_monday
        else "⚠️ Error Summary of the past 24 hours ⚠️"
    )
    client = boto3.client("sns")
    message = {
        "version": "1.0",
        "source": "custom",
        "content": {
            "textType": "client-markdown",
            "title": title,
            "description": summary,
        },
    }
    result = client.publish(TopicArn=arn, Message=json.dumps(message))
    logging.info(f"Published error summary to SNS topic {arn}: {result}")
