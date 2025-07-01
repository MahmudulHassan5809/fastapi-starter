from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import Response
from src.core.cache import ASYNC_CACHE_MANAGER, CacheTag
from src.core.error.codes import MAINTENANCE_MODE, UPDATE_REQUIRED
from src.core.error.exceptions import MaintenanceModeException, UpdateRequiredException
from src.core.error.format_error import ERROR_MAPPER
from starlette.middleware.base import BaseHTTPMiddleware

ALLOWED_VERSION_LIST = []


class MaintenanceModeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if any(
            excluded_path in request.url.path
            for excluded_path in [
                "app-settings",
                "health-check",
                "public",
                "admin",
                "callback",
                "webhook",
                "docs",
                "openapi.json",
                "forget-password",
                "reset-password",
            ]
        ):
            return await call_next(request)

        application_settings = await ASYNC_CACHE_MANAGER.get(CacheTag.APPLICATION_SETTINGS)

        if application_settings.get("IS_SYSTEM_IN_MAINTENANCE", {}).get("value") == "true":
            raise MaintenanceModeException(errors=ERROR_MAPPER.get(MAINTENANCE_MODE))
        if not request.headers.get("version-code") or (
            request.headers.get("version-code") not in ALLOWED_VERSION_LIST
        ):
            raise UpdateRequiredException(errors=ERROR_MAPPER.get(UPDATE_REQUIRED))

        return await call_next(request)
