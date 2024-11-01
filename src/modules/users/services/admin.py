from src.core.error.codes import USER_EXISTS
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import ERROR_MAPPER
from src.core.helpers.enums import ProfileStatusEnum
from src.core.security.password_handler import PasswordHandler
from src.core.service.base import BaseService
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import StaffCreate


class AdminUserService(BaseService):

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        super().__init__()
        self.repository: UserRepository = user_repository

    async def create_staff(self, data: StaffCreate) -> None:
        user_exists = await self.repository.get_by_field(
            filters={"email": data.email, "phone": data.phone}, use_or=True
        )

        if user_exists:
            raise ValidationException(errors=ERROR_MAPPER.get(USER_EXISTS))
        data.status = ProfileStatusEnum.ACTIVE
        hashed_password = PasswordHandler.hash(password=data.password)
        await self.repository.create(
            obj=User(password=hashed_password, **data.model_dump(exclude={"password"}))
        )
