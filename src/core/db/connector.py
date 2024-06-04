import logging
import typing
from sqlalchemy.ext import asyncio as sa
from .settings import Settings

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._engine = None

    async def create_engine(self) -> typing.AsyncIterator[sa.AsyncEngine]:
        logger.debug("Initializing SQLAlchemy engine")
        self._engine = sa.create_async_engine(
            url=self.settings.db_dsn,
            echo=self.settings.debug,
            echo_pool=self.settings.debug,
            pool_size=self.settings.db_pool_size,
            pool_pre_ping=self.settings.db_pool_pre_ping,
            max_overflow=self.settings.db_max_overflow,
        )
        logger.debug("SQLAlchemy engine has been initialized")
        try:
            yield self._engine
        finally:
            await self._engine.dispose()
            logger.debug("SQLAlchemy engine has been cleaned up")

    async def get_engine(self) -> sa.AsyncEngine:
        if not self._engine:
            # We ensure to create the engine only once and use it across the app's lifecycle
            async for engine in self.create_engine():
                self._engine = engine
        return self._engine

    async def get_session(self) -> typing.AsyncIterator[sa.AsyncSession]:
        engine = await self.get_engine()
        async with sa.AsyncSession(
            engine, expire_on_commit=False, autoflush=False
        ) as session:
            yield session
