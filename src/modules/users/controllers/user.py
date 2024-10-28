from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from src.core.di import Container
from src.modules.users.schemas import UserProfile
from src.modules.users.services import UserService

router = APIRouter(prefix="")


@router.get("/profile/", response_model=UserProfile)
@inject
async def profile(
    request: Request,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> Any:
    user_id = request.state.user["user_id"]
    return await user_service.get_profile(user_id=user_id)
