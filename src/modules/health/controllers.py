from typing import Any

from fastapi import APIRouter
from src.core.config import settings
from src.core.router_logging import LoggingApiRoute
from src.modules.health.schemas import HealthCheck

router = APIRouter(prefix="/health-check", tags=["Health Check"], route_class=LoggingApiRoute)


@router.get("/", response_model=HealthCheck)
def health_check() -> Any:
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "FastApi-Starter",
    }
