from fastapi import APIRouter, Depends

from src.core.dependencies.authentication import JWTBearer
from src.modules.users.controllers import user_router

api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(JWTBearer())],
)
