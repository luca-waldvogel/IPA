from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class QueryResponse(BaseModel, alias_generator=to_camel):
    query_id: str


class QueryResult(BaseModel):
    results: list[list[dict]]
    status: str


class LogInsights(BaseModel):
    timestamp: datetime
    level: str
    logger: str
    file: str
    line: int | None = None
    message: str
    extra: dict | None = None


class LogInsightsOutput(BaseModel, alias_generator=to_camel):
    pattern: str
    log_samples: str
    tokens: str
    sample_count: int

    @classmethod
    def from_insights_result(cls, result: list[dict]) -> Self:
        record = {item["field"].removeprefix("@"): item["value"] for item in result}
        return cls.model_validate(record)


class LogInsightsPattern(BaseModel):
    pattern: str
    log_groups: list[str]
    log_sample: LogInsights | None
    sample_count: int


class ErrorCount(BaseModel):
    error: str = Field(alias="field")
    count: int = Field(alias="value")

    def __str__(self) -> str:
        return f"{self.error}: {self.count}"
