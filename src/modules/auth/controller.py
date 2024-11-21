# pylint: disable=unused-argument
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.di import Container
from src.core.routing import LoggingApiRoute
from src.modules.auth.schemas import TokenResponse, UserLogin, UserRegister
from src.modules.auth.service import AuthService

router = APIRouter(prefix="", route_class=LoggingApiRoute)


@router.post("/register/", response_model=TokenResponse)
@inject
async def validate_otp_register(
    data: UserRegister,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> Any:
    return await auth_service.register(data)


@router.post("/login/", response_model=TokenResponse)
@inject
async def login(
    data: UserLogin,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> Any:
    return await auth_service.login(data=data)
