from fastapi import FastAPI
from src.core.config import settings
from src.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    contact={
        "email": settings.SUPER_USER_EMAIL,
    }
)


app.include_router(api_router, prefix=f"{settings.API_V1_STR}")
