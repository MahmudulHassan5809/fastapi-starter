from collections.abc import Sequence
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


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
    payload: dict[str, Any] | str
    headers: dict[str, Any]
    cert: tuple[str, str] | None = None
    verify: bool = True
    timeout: int = 5
    payload_key_type: Literal["json", "data"] = "json"


class S3UploadConfig(BaseModel):
    file_content: bytes
    bucket_name: str
    object_name: str
    content_type: str
    cloud_front_url: str | None = None


class PaginationMeta(BaseModel):
    total: int
    current_page: int
    next_page: int | None
    prev_page: int | None
    last_page: int
    extra: Any | None = None


class PaginatedResponse(BaseModel, Generic[T]):  # noqa
    data: Sequence[T]
    meta: PaginationMeta


class QueryParams(BaseModel):
    page: int = Field(1, ge=1, description="The page number to retrieve")
    page_size: int = Field(10, ge=1, le=100, description="The number of items per page")
    search: str | None = Field(None, description="The search query")
    filter_params: dict[str, Any] | None = None
    sorting: dict[str, str] | None = None

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size


class FilterOptions(BaseModel):
    filters: dict[str, Any]
    pagination: QueryParams | None = None
    search_fields: list[str] | None = None
    sorting: dict[str, str] | None = None
    prefetch: tuple[str, ...] | None = None
    use_or: bool = False
    distinct_on: str | None = None
    raw_query: str | None = None
    or_filters: set[str] | None = None
