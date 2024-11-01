from src.core.cache import Cache, CacheTag
from src.core.service.base import BaseService
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import UserProfile


class UserService(BaseService):
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        super().__init__()
        self.repository: UserRepository = user_repository

    async def get_profile(self, user_id: str) -> UserProfile:
        user_data_key = CacheTag.USER_DATA.value.format(user_id=user_id)
        data = await Cache.get(key=user_data_key)
        return UserProfile(**data)
