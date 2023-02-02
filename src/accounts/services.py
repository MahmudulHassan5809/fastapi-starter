from src.core.services.main_service import AppService
from src.accounts.models import UserCreate

class UserService(AppService):
    def create_user(self, data: UserCreate):
        pass