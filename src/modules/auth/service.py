from src.core.cache import Cache, CacheTag
from src.core.config import settings
from src.core.error.codes import USER_EXISTS
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import ERROR_MAPPER
from src.core.helpers.enums import ProfileStatusEnum
from src.core.security import JWTHandler, PasswordHandler
from src.core.service.base import BaseService
from src.modules.auth.schemas import (
    AccessTokenPayload,
    RefreshTokenPayload,
    TokenResponse,
    UserRegister,
)
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import UserProfile


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__()
        self.user_repository: UserRepository = user_repository

    async def set_cache(
        self, user_id: str, user_profile: UserProfile, tokens: TokenResponse
    ) -> None:
        user_data_key = CacheTag.USER_DATA.value.format(user_id=user_id)
        user_access_token_key = CacheTag.USER_ACCESS_TOKEN.value.format(user_id=user_id)
        user_refresh_token_key = CacheTag.USER_REFRESH_TOKEN.value.format(
            user_id=user_id
        )
        await Cache.set(
            key=user_data_key,
            value=user_profile.model_dump(),
            ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        await Cache.set(
            key=user_access_token_key,
            value=tokens.access_token,
            ttl=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        await Cache.set(
            key=user_refresh_token_key,
            value=tokens.refresh_token,
            ttl=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def register(self, data: UserRegister) -> TokenResponse:
        user_exists = await self.user_repository.get_by_field(
            filters={"email": data.email, "phone": data.phone}, use_or=True
        )

        if user_exists:
            raise ValidationException(errors=ERROR_MAPPER.get(USER_EXISTS))

        hashed_password = PasswordHandler.hash(password=data.password)

        user_create = UserRegister(
            password=hashed_password,
            status=ProfileStatusEnum.ACTIVE,
            **data.model_dump(exclude={"password"})
        )

        created_user = await self.user_repository.create(
            obj=User(**user_create.model_dump())
        )

        access_token = JWTHandler.encode(
            token_type="access",
            payload=AccessTokenPayload(
                user_id=created_user.id,
                email=created_user.email,
            ),
        )
        refresh_token = JWTHandler.encode(
            token_type="refresh",
            payload=RefreshTokenPayload(
                user_id=created_user.id,
            ),
        )
        tokens = TokenResponse(access_token=access_token, refresh_token=refresh_token)

        await self.set_cache(
            user_id=created_user.id,
            user_profile=UserProfile(**created_user.to_dict()),
            tokens=tokens,
        )

        return tokens
