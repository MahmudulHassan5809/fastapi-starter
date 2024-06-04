import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext import asyncio as sa

from src.core.config import Settings

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._engine: sa.AsyncEngine | None = None

    async def create_engine(self) -> AsyncIterator[sa.AsyncEngine]:
        logger.debug("Initializing SQLAlchemy engine")
        self._engine = sa.create_async_engine(
            url=self.settings.DB_DSN,
            echo=self.settings.DEBUG,
            echo_pool=self.settings.DEBUG,
            pool_size=self.settings.DB_POOL_SIZE,
            pool_pre_ping=self.settings.DB_POOL_PRE_PING,
            max_overflow=self.settings.DB_MAX_OVERFLOW,
        )
        logger.debug("SQLAlchemy engine has been initialized")
        try:
            yield self._engine
        finally:
            await self._engine.dispose()
            logger.debug("SQLAlchemy engine has been cleaned up")

    async def get_engine(self) -> sa.AsyncEngine:
        if not self._engine:
            async for engine in self.create_engine():
                self._engine = engine
        assert self._engine is not None  # Ensure that self._engine is not None
        return self._engine

    async def get_session(self) -> AsyncIterator[sa.AsyncSession]:
        engine = await self.get_engine()
        async with sa.AsyncSession(
            engine, expire_on_commit=False, autoflush=False
        ) as session:
            yield session
