from math import ceil

from src.core.error.codes import USER_EXISTS
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import ERROR_MAPPER
from src.core.helpers.enums import ProfileStatusEnum
from src.core.schemas.common import (
    PaginatedResponse,
    PaginationMeta,
    PaginationParams,
    ResponseMessage,
)
from src.core.security.password_handler import PasswordHandler
from src.core.service.base import BaseService
from src.modules.users.models import User
from src.modules.users.repository import UserRepository
from src.modules.users.schemas import AdminUserProfile, StaffCreate, UserProfile


class AdminUserService(BaseService):

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        super().__init__()
        self.repository: UserRepository = user_repository

    async def create_staff(self, data: StaffCreate) -> ResponseMessage:
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
        return ResponseMessage(message="Staff created successfully")

    async def get_staff_list(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[AdminUserProfile]:
        data, total = await self.repository.paginate_filter(
            filters={"is_staff": True}, pagination=pagination
        )
        last_page = ceil(total / pagination.page_size)

        next_page = pagination.page + 1 if pagination.page < last_page else None
        prev_page = pagination.page - 1 if pagination.page > 1 else None

        return PaginatedResponse(
            data=data,
            meta=PaginationMeta(
                total=total,
                current_page=pagination.page,
                next_page=next_page,
                prev_page=prev_page,
                last_page=last_page,
            ),
        )

    async def get_user_list(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[UserProfile]:
        data, total = await self.repository.paginate_filter(
            filters={"is_staff": False}, pagination=pagination
        )
        last_page = ceil(total / pagination.page_size)

        next_page = pagination.page + 1 if pagination.page < last_page else None
        prev_page = pagination.page - 1 if pagination.page > 1 else None

        return PaginatedResponse(
            data=data,
            meta=PaginationMeta(
                total=total,
                current_page=pagination.page,
                next_page=next_page,
                prev_page=prev_page,
                last_page=last_page,
            ),
        )
