from fastapi import APIRouter

from src.modules.auth.controller import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["User Auth"])
