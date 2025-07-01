from collections.abc import Callable
from typing import Any

from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from src.core.config import settings
from src.core.error.exceptions import CustomException, DatabaseError
from src.core.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CustomErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Any]) -> Any:
        try:
            return await call_next(request)

        except SQLAlchemyError:
            return await self._handle_exception(
                request,
                message="Unexpected SQLAlchemy error occurred",
                status_code=500,
            )

        except CustomException as exc:
            error_msg = (
                "Database error"
                if isinstance(exc, DatabaseError) and not settings.DEBUG
                else exc.message
            )
            return await self._handle_exception(
                request,
                message=f"CustomException: {error_msg}",
                status_code=exc.code,
                user_message="Something went wrong" if exc.code == 500 else exc.message,
                errors=None if exc.code == 500 else exc.errors,
            )

        except Exception as exc:  # pylint: disable=broad-exception-caught
            return await self._handle_exception(
                request,
                message=f"Unhandled Exception: {repr(exc)}",
                status_code=500,
            )

    async def _handle_exception(
        self,
        request: Request,
        message: str,
        status_code: int,
        user_message: str | None = None,
        errors: Any = None,
    ) -> JSONResponse | HTMLResponse:
        client_ip = request.headers.get(
            "X-Forwarded-For", request.client.host if request.client else None
        )
        logger.error(message, client_ip=client_ip)
        return JSONResponse(
            status_code=status_code,
            content={
                "message": user_message or "Something went wrong",
                "errors": errors,
            },
        )
