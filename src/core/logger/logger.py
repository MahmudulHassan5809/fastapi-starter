import datetime
import json
import logging
from typing import Any

import stackprinter

from src.core.schemas.common import BaseJsonLogSchema

LEVEL_TO_NAME = {
    logging.CRITICAL: "Critical",
    logging.ERROR: "Error",
    logging.WARNING: "Warning",
    logging.INFO: "Information",
    logging.DEBUG: "Debug",
    logging.NOTSET: "Trace",
}


class JSONLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord, *args: Any, **kwargs: Any) -> str:
        _ = args
        _ = kwargs
        log_object: dict[Any, Any] = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=True, indent=4)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict[Any, Any]:
        now = (
            datetime.datetime.fromtimestamp(record.created)
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )
        message = record.getMessage()
        duration = record.duration if hasattr(record, "duration") else record.msecs

        json_log_fields = BaseJsonLogSchema(
            thread=record.process,
            timestamp=now,
            level_name=LEVEL_TO_NAME[record.levelno],
            message=message,
            source_log=record.name,
            duration=duration,
        )
        if hasattr(record, "props"):
            json_log_fields.props = record.props

        if record.exc_info:
            json_log_fields.exceptions = stackprinter.format(
                record.exc_info,
                suppressed_paths=[r"lib/python.*"],
                add_summary=False,
            ).split("\n")

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        json_log_object = json_log_fields.model_dump(
            exclude_unset=True,
            by_alias=True,
        )
        if hasattr(record, "request_json_fields"):
            json_log_object.update(record.request_json_fields)
        return json_log_object
