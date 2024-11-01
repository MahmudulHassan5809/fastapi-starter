from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from src.core.decorators.check_permission import check_permission
from src.core.dependencies.get_current_user import get_current_user
from src.core.di import Container
from src.core.permissions.enums import UserPermission
from src.core.schemas.common import PaginatedResponse, PaginationParams, ResponseMessage
from src.modules.users.models import User
from src.modules.users.schemas import AdminUserProfile, StaffCreate
from src.modules.users.services import AdminUserService

router = APIRouter(prefix="")


@router.post("/staffs/", response_model=ResponseMessage)
@inject
@check_permission(UserPermission.CREATE)
async def create_staff(
    _request: Request,
    data: StaffCreate,
    admin_user_service: AdminUserService = Depends(
        Provide[Container.admin_user_service]
    ),
    _user: User = Depends(get_current_user),
) -> Any:
    return await admin_user_service.create_staff(data=data)


@router.get("/staffs/", response_model=PaginatedResponse[AdminUserProfile])
@inject
@check_permission(UserPermission.READ)
async def get_staff_list(
    _request: Request,
    admin_user_service: AdminUserService = Depends(
        Provide[Container.admin_user_service]
    ),
    user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
) -> Any:
    return await admin_user_service.get_staff_list(pagination=pagination)
