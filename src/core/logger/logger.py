import json
from typing import Any

import structlog
from structlog import processors
from structlog.processors import JSONRenderer
from structlog.typing import EventDict

from src.core.config import settings


# Define custom processor to censor sensitive information in response data
def censor_sensitive_data(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    response_body = event_dict.get("response_body")
    request_body = event_dict.get("request_body")

    if isinstance(response_body, list):
        event_dict["response_body"] = response_body[1:2]
    if isinstance(response_body, dict):
        response_body = {
            key: value
            for key, value in response_body.items()
            if key.lower() not in {"password"} and "token" not in key.lower()
        }
        event_dict["response_body"] = response_body

    if isinstance(request_body, dict):
        request_body["password"] = "censored"

    if event_dict.get("request_header", {}).get("authorization"):
        event_dict["request_header"]["authorization"] = "censored"

    return event_dict


shared_processors: list[Any] = [
    processors.add_log_level,
    processors.StackInfoRenderer(),
    processors.TimeStamper(fmt="iso"),
    processors.EventRenamer("msg"),
    processors.CallsiteParameterAdder(
        [
            processors.CallsiteParameter.FUNC_NAME,
            processors.CallsiteParameter.LINENO,
            processors.CallsiteParameter.FILENAME,
        ]
    ),
    censor_sensitive_data,
]

console_log_formatter = structlog.dev.ConsoleRenderer()
json_log_formatter = JSONRenderer(serializer=json.dumps, indent=2)


def configure_console_logger() -> Any:
    return structlog.wrap_logger(
        structlog.get_logger(),
        processors=[*shared_processors, console_log_formatter],
    )


def configure_json_logger() -> Any:
    return structlog.wrap_logger(
        structlog.get_logger(),
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.dict_tracebacks,
            json_log_formatter,
        ],
    )


def configure_logger() -> Any:
    if settings.APP_ENV == "dev":
        return configure_console_logger()
    return configure_json_logger()


logger = configure_logger()
