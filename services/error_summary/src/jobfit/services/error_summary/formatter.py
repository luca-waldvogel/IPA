import json

from jobfit.model.error_summary import (
    LogInsights,
    LogInsightsOutput,
    LogInsightsPattern,
)


def _parse_log_event(log_event_str: str) -> LogInsights:
    space_idx = log_event_str.index(" ")
    json_str = log_event_str[space_idx + 1 :]
    log_data = json.loads(json_str)

    return LogInsights(
        timestamp=log_data["timestamp"],
        level=log_data["level"],
        logger=log_data["logger"],
        file=log_data["file"],
        line=log_data.get("line"),
        message=log_data["message"],
        extra=log_data.get("extra"),
    )


def _parse_log_samples(log_samples_str: str) -> LogInsights | None:
    try:
        samples = json.loads(log_samples_str)
        if not samples or len(samples) == 0:
            return None
        return _parse_log_event(samples[0]["logEvent"])
    except json.JSONDecodeError:
        return None
    except KeyError:
        return None
    except ValueError:
        return None


def _match_log_groups(
    output: LogInsightsOutput, possible_log_groups: list[str]
) -> list[str]:
    return [
        lg for lg in possible_log_groups if lg in output.pattern or lg in output.tokens
    ]


def format_log_insights_output(
    outputs: list[LogInsightsOutput],
    possible_log_groups: list[str],
) -> list[LogInsightsPattern]:
    result = []
    for output in outputs:
        result.append(
            LogInsightsPattern(
                pattern=output.pattern,
                log_groups=_match_log_groups(output, possible_log_groups),
                log_sample=_parse_log_samples(output.log_samples),
                sample_count=output.sample_count,
            )
        )
    return result
