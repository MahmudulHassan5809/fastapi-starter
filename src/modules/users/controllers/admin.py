from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from src.core.decorators.check_permission import check_permission
from src.core.dependencies.get_current_user import get_current_user
from src.core.di import Container
from src.core.permissions.enums import UserPermission
from src.modules.users.models import User
from src.modules.users.services import UserService

router = APIRouter(prefix="")


@router.post("/staffs/", response_model=None)
@inject
@check_permission(UserPermission.CREATE)
async def profile(
    request: Request,
    user_service: UserService = Depends(Provide[Container.user_service]),
    user: User = Depends(get_current_user),
) -> Any:
    user_id = request.state.user["user_id"]
