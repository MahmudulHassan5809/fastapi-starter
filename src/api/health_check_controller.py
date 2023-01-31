from fastapi import APIRouter
from src.core.config import settings
from src.schemas.health_check import HealthCheck

router = APIRouter(
    prefix="/health-check",
    tags=['Health Check']
)


@router.get("/", response_model=HealthCheck)
async def health_check():
   return {
       "name": settings.PROJECT_NAME,
       "version": settings.VERSION,
       "description": settings.DESCRIPTION
    }


