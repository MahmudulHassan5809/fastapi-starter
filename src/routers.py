from fastapi import APIRouter

from src.modules.auth.routers import api_router as user_auth_router
from src.modules.health.controllers import router as health_router

api_router = APIRouter()


api_router.include_router(health_router)
api_router.include_router(user_auth_router)
