from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt

from src.core.config import settings
from src.core.error.exceptions import JWTError
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

        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
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
            return jwt.decode(
                token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm]
            )
        except jwt.PyJWTError as exception:
            raise JWTError() from exception

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
            raise JWTError() from exception
