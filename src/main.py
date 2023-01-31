from fastapi import FastAPI
from src.core.config import settings
from src.api.router import api_router

app = FastAPI()


app.include_router(api_router, prefix=f"{settings.API_V1_STR}")
