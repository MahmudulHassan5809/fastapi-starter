import http
import json
import time
import uuid
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from src.core.error.exceptions import CustomException, DatabaseError
from src.core.logger import logger


class LoggingApiRoute(APIRoute):
    def get_route_handler(self) -> Callable[..., Any]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(
            request: Request,
        ) -> Response:  # pylint: disable=too-many-locals
            host = getattr(getattr(request, "client", None), "host", None)
            port = getattr(getattr(request, "client", None), "port", None)

            url = (
                f"{request.url.path}?{request.query_params}"
                if request.query_params
                else request.url.path
            )

            headers = dict(request.scope["headers"])
            request_id = headers.get(b"x-request-id")

            if not request_id:
                request_id = str(uuid.uuid4())
                headers[b"x-request-id"] = bytes(request_id, "utf-8")
            else:
                request_id = str(request_id, "utf-8")

            request.scope["headers"] = list(headers.items())

            request_body = await request.body()
            try:
                request_body_dict = json.loads(request_body)
            except (json.JSONDecodeError, UnicodeDecodeError):
                request_body_dict = {}
            before = time.time()

            try:
                response: Response = await original_route_handler(request)
            except (Exception, CustomException) as exc:
                duration = time.time() - before
                duration = format(duration, ".2f")  # type: ignore
                error = str(exc)
                if isinstance(exc, CustomException):
                    if isinstance(exc, DatabaseError):
                        error = "Database error"
                    status_code = exc.code
                elif isinstance(exc, RequestValidationError):
                    status_code = 400
                else:
                    status_code = 500
                logger.error(
                    "request_failed",
                    request_id=request_id,
                    status_code=status_code,
                    request_url=f"{host}:{port}",
                    method=request.method,
                    path=url,
                    duration=f"{duration}s",
                    # request_header=dict(request.headers),
                    request_body=request_body_dict,
                    client_ip=request.headers.get(
                        "X-Forwarded-For",
                        request.client.host if request.client else None,
                    ),
                    error=error,
                    response_body=None,
                )

                # Re-raise the exception to trigger FastAPI's exception handlers
                raise

            duration = time.time() - before
            duration_str = format(duration, ".2f")
            response.headers["X-Process-Time"] = duration_str
            response.headers["X-Request-Id"] = request_id

            try:
                response_body = json.loads(response.body)
            except (json.JSONDecodeError, AttributeError):
                response_body = {}

            try:
                status_phrase = http.HTTPStatus(response.status_code).phrase
            except ValueError:
                status_phrase = ""

            # Log the details in JSON format
            logger.info(
                "request_processed",
                request_id=request_id,
                request_url=f"{host}:{port}",
                method=request.method,
                path=url,
                status_code=response.status_code,
                status_phrase=status_phrase,
                duration=f"{duration}s",
                # request_header=dict(request.headers),
                request_body=request_body_dict,
                client_ip=request.headers.get(
                    "X-Forwarded-For", request.client.host if request.client else None
                ),
                # response_header=dict(response.headers),
                response_body=response_body,
            )
            return response

        return custom_route_handler
