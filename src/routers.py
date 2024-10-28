from fastapi import APIRouter

from src.modules.auth.router import api_router as auth_router
from src.modules.users.router import api_router as user_router

api_router = APIRouter()


api_router.include_router(auth_router)
api_router.include_router(user_router)
