from fastapi import FastAPI
from src.core.config import settings
from src.api.router import api_router
from src.db.db_session import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(api_router, prefix=f"{settings.API_V1_STR}")
