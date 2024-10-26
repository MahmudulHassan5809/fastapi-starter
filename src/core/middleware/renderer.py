import json
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class ResponseMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.url.path in ["/openapi.json", "/docs", "/redoc"]:
            return await call_next(request)

        response = await call_next(request)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        try:
            response_json = json.loads(response_body.decode("utf-8"))
            data: dict[str, Any] = {
                "success": (response.status_code // 100) not in (4, 5)
            }
            if data["success"]:
                data["data"] = response_json
                data["message"] = "OK"
            else:
                data["message"] = (
                    response_json.get("message") or response_json.get("detail")
                    if response_json
                    else None
                )
                data["error"] = response_json.get("errors") if response_json else None
                data["data"] = None

            data["code"] = response.status_code
            data["meta_info"] = None
            modified_response = json.dumps(data).encode("utf-8")
            response.headers["Content-Length"] = str(len(modified_response))
            return Response(
                content=modified_response,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
        except Exception:  # pylint: disable=broad-exception-caught
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
