from math import ceil

from src.core.error.codes import USER_EXISTS
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import ERROR_MAPPER
from src.core.helpers.enums import ProfileStatusEnum
from src.core.schemas.common import (
    FilterOptions,
    PaginatedResponse,
    PaginationMeta,
    QueryParams,
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
        self, query_params: QueryParams
    ) -> PaginatedResponse[AdminUserProfile]:
        filters = {"is_staff": True}
        if query_params.filter_params:
            filters.update(query_params.filter_params)
        data, total = await self.repository.paginate_filter(
            filter_options=FilterOptions(
                filters=filters,
                query_params=query_params,
                sorting=query_params.sorting,
            )
        )
        last_page = ceil(total / query_params.page_size)

        next_page = query_params.page + 1 if query_params.page < last_page else None
        prev_page = query_params.page - 1 if query_params.page > 1 else None

        return PaginatedResponse(
            data=data,
            meta=PaginationMeta(
                total=total,
                current_page=query_params.page,
                next_page=next_page,
                prev_page=prev_page,
                last_page=last_page,
            ),
        )

    async def get_user_list(
        self, query_params: QueryParams
    ) -> PaginatedResponse[UserProfile]:
        filters = {"is_staff": False}
        if query_params.filter_params:
            filters.update(query_params.filter_params)
        data, total = await self.repository.paginate_filter(
            filter_options=FilterOptions(
                filters=filters,
                query_params=query_params,
                sorting=query_params.sorting,
            )
        )
        last_page = ceil(total / query_params.page_size)

        next_page = query_params.page + 1 if query_params.page < last_page else None
        prev_page = query_params.page - 1 if query_params.page > 1 else None

        return PaginatedResponse(
            data=data,
            meta=PaginationMeta(
                total=total,
                current_page=query_params.page,
                next_page=next_page,
                prev_page=prev_page,
                last_page=last_page,
            ),
        )
