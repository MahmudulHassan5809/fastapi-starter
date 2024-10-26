from collections.abc import Callable
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.core.error.exceptions import CustomException
from src.core.logger import logger


class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Any:
        try:
            response = await call_next(request)
            return response
        except SQLAlchemyError as exc:
            return JSONResponse(
                status_code=400,
                content={
                    "message": str(exc.__dict__.get("orig", str(exc))),
                },
            )
        except CustomException as exc:
            return JSONResponse(
                status_code=exc.code,
                content={
                    "message": exc.message,
                    "errors": exc.errors,
                },
            )
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.exception("An unexpected error occurred: %s", exc)
            return JSONResponse(
                status_code=500,
                content={
                    "message": repr(exc),
                    "errors": None,
                },
            )
