from pydantic import BaseModel


class LLMSummarizedError(BaseModel):
    pattern_index: int
    error: str
    summary: str


class SummarizedError(BaseModel):
    error: str
    count: int
    summary: str
    log_groups: list[str]


class ErrorSummaryPromptOutput(BaseModel):
    summaries: list[LLMSummarizedError]
