from fastapi import APIRouter

from src.modules.health.controllers import router as health_router

api_router = APIRouter()


api_router.include_router(health_router)
