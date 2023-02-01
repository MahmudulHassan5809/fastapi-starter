from fastapi import APIRouter

from src.api import health_check_controller
from src.accounts.api.router import api_router as accounts_router


api_router = APIRouter()



api_router.include_router(health_check_controller.router)
api_router.include_router(accounts_router)