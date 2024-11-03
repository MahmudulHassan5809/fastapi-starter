"""Fast Api module"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from src.core.cache.cache_manager import Cache
from src.core.cache.redis_backend import RedisBackend
from src.core.config import settings
from src.core.di import Container
from src.core.middleware import (
    CustomErrorMiddleware,
    ResponseMiddleware,
    validation_exception_handler,
)
from src.routers import api_router


class FastAPIApp:
    def __init__(self) -> None:
        self.app = FastAPI(
            title="Fast API Starter APP",
            description="Fast API Starter APP",
            version=settings.VERSION,
            debug=settings.DEBUG,
            docs_url=None if settings.APP_ENV == "prod" else "/docs",
            redoc_url=None if settings.APP_ENV == "prod" else "/redoc",
            # middleware=self.make_middleware(),
        )
        self.make_middleware()
        self.container = self.create_dependency()
        self.app.container = self.container

    def make_middleware(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
        )
        self.app.add_middleware(CustomErrorMiddleware)
        self.app.add_middleware(ResponseMiddleware)

    def create_dependency(self) -> Container:
        return Container()

    def init_routers(self) -> None:
        self.app.include_router(api_router, prefix=f"/api/{settings.VERSION}")

    def init_cache(self) -> None:
        Cache.init(backend=RedisBackend(url=settings.REDIS_URL))

    def create_app(self) -> FastAPI:
        self.init_routers()
        self.app.add_exception_handler(
            RequestValidationError, validation_exception_handler
        )
        self.init_cache()
        return self.app


fastapi_app = FastAPIApp()
app = fastapi_app.create_app()
