from src.core.service.base import BaseService
from src.modules.auth.schemas import TokenResponse, UserLogin
from src.modules.users.repository import UserRepository


class UserAuthService(BaseService):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__()
        self.user_repository: UserRepository = user_repository

    async def login(self, data: UserLogin) -> TokenResponse:
        return TokenResponse(
            access_token="",
            refresh_token="",
            user_id="",
            profile_status="",
        )
