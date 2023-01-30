from fastapi import APIRouter

from src.api import health_check_controller

api_router = APIRouter()

api_router.include_router(health_check_controller.router)
