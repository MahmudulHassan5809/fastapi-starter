from typing import Any

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
