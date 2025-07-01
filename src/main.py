from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from src.core.cache.cache_manager import ASYNC_CACHE_MANAGER, SYNC_CACHE_MANAGER
from src.core.cache.redis_backend import RedisBackendAsync, RedisBackendSync
from src.core.config import settings
from src.core.middleware import (
    CustomErrorMiddleware,
    ResponseMiddleware,
    validation_exception_handler,
)
from src.routers import api_router


class FastAPIApp:
    def __init__(self) -> None:
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            description=settings.PROJECT_NAME,
            version=settings.VERSION,
            debug=settings.DEBUG,
            docs_url=f"/api/{settings.VERSION}/docs" if settings.DEBUG else None,
            redoc_url=f"/api/{settings.VERSION}/redoc" if settings.DEBUG else None,
        )
        self.validation_error_handler()
        self.make_middleware()
        self.create_dependency()

    def validation_error_handler(self) -> None:
        self.app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def make_middleware(self) -> None:
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"],
        )
        # self.app.add_middleware(MaintenanceModeMiddleware)
        self.app.add_middleware(CustomErrorMiddleware)
        self.app.add_middleware(ResponseMiddleware)

    def create_dependency(self) -> None:
        """Will pass di container."""

    def init_cache(self) -> None:
        ASYNC_CACHE_MANAGER.init(backend=RedisBackendAsync(url=settings.REDIS_URL))
        SYNC_CACHE_MANAGER.init(backend=RedisBackendSync(url=settings.PERSIST_REDIS_URL))

    def init_routers(self) -> None:
        self.app.include_router(api_router, prefix=f"/api/{settings.VERSION}")

    def create_app(self) -> FastAPI:
        self.init_routers()
        self.init_cache()
        return self.app


fastapi_app = FastAPIApp()
app = fastapi_app.create_app()
