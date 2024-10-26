# pylint: disable=unused-argument
from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from src.core.di import Container
from src.modules.auth.service import AuthService
from src.modules.auth.schemas import TokenResponse, UserRegister

router = APIRouter(prefix="")


@router.post("/register/", response_model=TokenResponse)
@inject
async def validate_otp_register(
    data: UserRegister,
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> Any:
    return await auth_service.register(data)
