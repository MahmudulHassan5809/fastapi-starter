import logging
import sys
from logging.config import dictConfig

from src.core.config import settings

from .logger import JSONLogFormatter

LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JSONLogFormatter,
        },
    },
    "handlers": {
        "json": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "main": {
            "handlers": ["json"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}


dictConfig(LOG_CONFIG)
logger = logging.getLogger("main")


__all__ = ["logger", "JSONLogFormatter"]
