from fastapi import APIRouter
from src.modules.auth.controllers import user_auth_router

api_router = APIRouter(prefix="/auth")


api_router.include_router(user_auth_router, tags=["User Auth"])
