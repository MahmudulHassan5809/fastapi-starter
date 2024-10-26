from src.core.service.base import BaseService
from src.modules.auth.schemas import TokenResponse, UserRegister
from src.modules.users.repository import UserRepository


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__()
        self.user_repository: UserRepository = user_repository

    async def register(self, data: UserRegister) -> TokenResponse:
        print(data)
