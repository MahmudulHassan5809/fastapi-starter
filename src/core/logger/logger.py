import json
from typing import Any

import structlog
from src.core.config import settings
from structlog import processors
from structlog.processors import JSONRenderer
from structlog.typing import EventDict


# Define custom processor to censor sensitive information in response data
def censor_sensitive_data(_: Any, __: Any, event_dict: EventDict) -> EventDict:
    response_body = event_dict.get("response_body")
    request_body = event_dict.get("request_body")

    if isinstance(response_body, list):
        event_dict["response_body"] = response_body[1:2]
    if (
        response_body
        and isinstance(response_body, dict)
        and isinstance(response_body.get("data"), list)
    ):
        event_dict["response_body"]["data"] = response_body["data"][1:2]
    if isinstance(response_body, dict):
        response_body = {
            key: value
            for key, value in response_body.items()
            if all(substring not in key.lower() for substring in ("password", "token"))
        }
        event_dict["response_body"] = response_body

        for key in ["password", "access_token", "refresh_token", "token", "id_token"]:
            if key in response_body:
                response_body[key] = "censored"

    if isinstance(request_body, dict):
        for key in ["password", "token"]:
            if key in request_body:
                request_body[key] = "censored"
        if request_body.get("last_logged_metadata"):
            request_body["last_logged_metadata"]["fcm_token"] = "censored"

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
json_log_formatter = JSONRenderer(serializer=json.dumps)


def configure_console_logger() -> Any:
    structlog.configure(
        processors=[*shared_processors, console_log_formatter],
    )
    return structlog.get_logger()


def configure_json_logger() -> Any:
    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.format_exc_info,
            structlog.processors.dict_tracebacks,
            json_log_formatter,
        ]
    )
    return structlog.get_logger()


def configure_logger() -> Any:
    if settings.DEBUG:
        return configure_console_logger()
    return configure_json_logger()


logger = configure_logger()
