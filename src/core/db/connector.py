import contextlib
from collections.abc import AsyncIterator
from typing import TypeVar

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings
from src.core.error.exceptions import DatabaseError


class Base(DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""


ModelType = TypeVar("ModelType", bound=Base)  # pylint: disable=invalid-name


class Database:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self._engine: AsyncEngine | None = create_async_engine(url=db_url, echo=settings.DEBUG)
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    async def close(self) -> None:
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception as err:
            await session.rollback()
            raise DatabaseError(message=f"An error occurred during the session {err}") from err
        finally:
            await session.close()
