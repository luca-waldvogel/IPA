from typing import override

from pydantic import BaseModel

from jobfit.llm import PromptProgram
from jobfit.llm.openai import GptParams, get_negative_unicode_logit_bias
from jobfit.model.error_summary import (
    ErrorCount,
    ErrorSummaryPromptOutput,
    LogInsightsPattern,
    SummarizedError,
)

from .config import ERROR_SUMMARY_MAX_TOKENS


class ErrorSummaryRequest(BaseModel):
    error_patterns: list[LogInsightsPattern]
    http_errors: list[ErrorCount]


class ErrorSummaryProgram(
    PromptProgram[ErrorSummaryRequest, ErrorSummaryPromptOutput, str]
):
    system = """You are an application log analysis expert. You are given a list of error patterns from AWS CloudWatch Logs Insights. Each pattern represents a class of recurring errors, with a sample log entry.

Your task is to produce exactly one LLMSummarizedError for EACH pattern — no pattern may be skipped.

For each pattern, produce a LLMSummarizedError with:
- `pattern_index`: the index of the pattern as shown in the input
- `error`: a short, canonical error message identifying this class of error (e.g. "JWT token expired", "GPT output validation failure: empty JSON")
- `summary`: a concise explanation (1 short sentence) of what the error is and what likely caused it

Do not invent information not present in the patterns.

IMPORTANT: Every pattern index from 1 to N must appear exactly once in the output. Before finalizing, verify that the sorted list of all pattern_index values equals [1, 2, ..., N]."""

    user = "<patterns>{patterns}</patterns>"

    params = [
        GptParams(
            temperature=0,
            recover_json=False,
            logit_bias=get_negative_unicode_logit_bias(),
            max_tokens=ERROR_SUMMARY_MAX_TOKENS,
        )
    ]

    @override
    def map_input(self, input: ErrorSummaryRequest) -> dict | PromptProgram.SkipWith:
        if not input.error_patterns:
            return self.skip_with(self._format_no_errors_found(input.http_errors))

        return {
            "patterns": self._format_patterns(
                self._indexed_patterns(input.error_patterns)
            ),
        }

    @override
    def map_output(
        self, prompt_output: ErrorSummaryPromptOutput, input: ErrorSummaryRequest
    ) -> str:
        patterns_by_index = self._indexed_patterns(input.error_patterns)
        expected = len(patterns_by_index)
        indices = sorted(s.pattern_index for s in prompt_output.summaries)
        if indices != list(range(1, expected + 1)):
            raise ValueError(
                f"Pattern indices in output do not match input. Expected 1–{expected}, got {indices}"
            )
        summaries = [
            SummarizedError(
                error=summary.error,
                summary=summary.summary,
                count=patterns_by_index[summary.pattern_index].sample_count,
                log_groups=patterns_by_index[summary.pattern_index].log_groups,
            )
            for summary in prompt_output.summaries
        ]
        return self._format_summary(summaries, input)

    def _format_summary(
        self, summaries: list[SummarizedError], input: ErrorSummaryRequest
    ) -> str:
        lines = []
        for s in sorted(summaries, key=lambda x: x.count, reverse=True):
            log_groups = " / ".join(s.log_groups)
            lines.append(f"*{s.error}*")
            lines.append(f">Count: {s.count}")
            lines.append(f">Log Group: {log_groups}")
            lines.append(f">{s.summary}")
            lines.append("")

        lines = self._format_http_errors(lines, input.http_errors)
        return "\n".join(lines).rstrip()

    def _format_no_errors_found(self, http_errors: list[ErrorCount]) -> str:
        lines = ["No errors found (besides HTTP errors).", ""]
        lines = self._format_http_errors(lines, http_errors)
        return "\n".join(lines).rstrip()

    @staticmethod
    def _format_http_errors(
        lines: list[str], http_errors: list[ErrorCount]
    ) -> list[str]:
        lines.append("*HTTP Errors*")
        for error in http_errors:
            lines.append(f">{error.error}: {error.count}")
        return lines

    @staticmethod
    def _indexed_patterns(
        patterns: list[LogInsightsPattern],
    ) -> dict[int, LogInsightsPattern]:
        return {i: p for i, p in enumerate(patterns, start=1)}

    @staticmethod
    def _format_patterns(patterns: dict[int, LogInsightsPattern]) -> str:
        lines = []
        for i, p in patterns.items():
            lines.append(f'<pattern index="{i}">')
            lines.append(f"  pattern: {p.pattern}")
            if p.log_sample:
                s = p.log_sample
                lines.append("  sample_log:")
                lines.append(f"    timestamp: {s.timestamp.isoformat()}")
                lines.append(f"    level: {s.level}")
                lines.append(f"    file: {s.file}:{s.line or '?'}")
                lines.append(f"    message: {s.message}")
            lines.append("</pattern>")
        return "\n".join(lines)
