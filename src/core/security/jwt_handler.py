from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from src.core.config import settings
from src.core.error.codes import UNAUTHORIZED_ERROR
from src.core.error.exceptions import JWTError
from src.core.error.format_error import ERROR_MAPPER
from src.core.logger import logger
from src.modules.auth.schemas import AccessTokenPayload, RefreshTokenPayload


class JWTHandler:
    secret_key = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM
    access_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def encode(
        token_type: Literal["access", "refresh"],
        payload: AccessTokenPayload | RefreshTokenPayload,
    ) -> str:
        expire_minutes = (
            JWTHandler.access_expire_minutes
            if token_type == "access"
            else JWTHandler.refresh_expire_minutes
        )

        expire = datetime.now(UTC) + timedelta(minutes=expire_minutes)
        payload.exp = expire
        return str(
            jwt.encode(
                payload.model_dump(),
                JWTHandler.secret_key,
                algorithm=JWTHandler.algorithm,
            )
        )

    @staticmethod
    def decode(token: str) -> Any:
        try:
            return jwt.decode(token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm])
        except jwt.PyJWTError as exception:
            logger.error("JWK invalid %s", exception)
            raise JWTError(errors=ERROR_MAPPER[UNAUTHORIZED_ERROR]) from exception

    @staticmethod
    def decode_expired(token: str) -> Any:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
        except jwt.PyJWTError as exception:
            raise JWTError(errors=ERROR_MAPPER[UNAUTHORIZED_ERROR]) from exception
