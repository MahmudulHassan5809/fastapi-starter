from fastapi import APIRouter

from src.modules.auth.router import api_router as auth_router

api_router = APIRouter()


api_router.include_router(auth_router)
