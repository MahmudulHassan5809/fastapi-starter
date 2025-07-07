from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from src.core.di import Container
from src.core.router_logging import LoggingApiRoute
from src.modules.auth.schemas import TokenResponse, UserLogin
from src.modules.auth.services import UserAuthService

router = APIRouter(prefix="", route_class=LoggingApiRoute)


@router.post("/login/", response_model=TokenResponse)
@inject
async def login(
    data: UserLogin,
    user_auth_service: UserAuthService = Depends(Provide[Container.user_auth_service]),
) -> Any:
    return await user_auth_service.login(data=data)
