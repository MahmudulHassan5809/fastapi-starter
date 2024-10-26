from typing import Any, cast

import requests

from src.core.error.exceptions import RequestError
from src.core.logger import logger
from src.core.schemas.common import HttpRequestConfig


class SendRequest:
    def __call__(self, config: HttpRequestConfig) -> dict[str, Any]:
        try:
            request_params = {
                "url": config.url,
                "json": config.payload,
                "headers": config.headers,
                "verify": config.verify,
                "timeout": 5,
            }

            if config.method.upper() != "POST":
                request_params["params"] = request_params.pop("json")

            if config.cert:
                request_params["cert"] = config.cert

            if config.method.upper() == "POST":
                response = requests.post(**request_params)
            elif config.method.upper() == "GET":
                response = requests.get(**request_params)
            elif config.method.upper() == "DELETE":
                response = requests.delete(**request_params)
            else:
                raise ValueError("Invalid HTTP method. Supported methods: POST, GET")
            logger.info("nagad send request response: %s", {response.content})
            json_response = cast(dict[str, Any], response.json())
            if response.status_code != 200:
                raise RequestError(
                    message=f"HTTP error {response.status_code}: {json_response}"
                )
            return json_response
        except Exception as e:
            raise RequestError(message=f"Request error: {str(e)}") from e
