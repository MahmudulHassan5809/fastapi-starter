from fastapi import APIRouter, Depends
from src.accounts.schemas import Token, UserLogin
from src.accounts.services import UserService
from src.accounts.dependencies import get_user_service

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=Token)
async def login(
    user_credentials:  UserLogin, 
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.login(user_credentials)

