from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


class BaseJsonLogSchema(BaseModel):
    model_config = {"populate_by_name": True}
    thread: int | str
    level_name: str
    message: str
    source_log: str
    timestamp: str = Field(..., alias="@timestamp")
    duration: int
    exceptions: list[str] | str | None = None
    props: dict[str, str] | None = None


class ResponseMessage(BaseModel):
    message: str


class HttpRequestConfig(BaseModel):
    method: str
    url: str
    payload: dict[str, Any]
    headers: dict[str, Any]
    cert: tuple[str, str] | None = None
    verify: bool = True
    timeout: int = 5


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="The page number to retrieve")
    page_size: int = Field(10, ge=1, le=100, description="The number of items per page")

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size


T = TypeVar("T")


class PaginationMeta(BaseModel):
    total: int
    current_page: int
    next_page: int | None
    prev_page: int | None
    last_page: int


class PaginatedResponse(BaseModel, Generic[T]):
    data: Sequence[T]
    meta: PaginationMeta
