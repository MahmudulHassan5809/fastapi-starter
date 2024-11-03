from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.cache import Cache, CacheTag
from src.core.error.codes import FORBIDDEN_ERROR
from src.core.error.exceptions import JWTError
from src.core.error.format_error import ERROR_MAPPER
from src.core.logger import logger
from src.core.security.jwt_handler import JWTHandler
from src.modules.auth.schemas import AccessTokenPayload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True) -> None:
        super().__init__(auto_error=auto_error)

    async def verify_jwt(self, token: str) -> tuple[bool, AccessTokenPayload | None]:
        try:
            payload: AccessTokenPayload = AccessTokenPayload(
                **JWTHandler.decode(token=token)
            )

            key = CacheTag.USER_ACCESS_TOKEN.value.format(user_id=payload.user_id)
            user_data_key = CacheTag.USER_DATA.value.format(user_id=payload.user_id)
            if (
                token != await Cache.get(key=key)
                or payload.sub != "access"
                or not await Cache.get(key=user_data_key)
            ):
                return False, None
            return True, payload
        except (JWTError, Exception) as err:  # pylint: disable=broad-exception-caught
            logger.error("JWK invalid %s", err)
            return False, None

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        jwt_token = credentials.credentials
        is_verified_jwt, decoded_data = await self.verify_jwt(token=jwt_token)
        if not is_verified_jwt or not decoded_data:
            raise JWTError(errors=ERROR_MAPPER[FORBIDDEN_ERROR])
        request.state.user = decoded_data.model_dump(exclude={"exp"})
        return credentials
