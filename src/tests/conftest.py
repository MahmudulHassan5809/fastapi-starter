from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from src.core.cache import AsyncCacheManager, CacheTag
from src.core.config import settings
from src.core.db import Base, Database
from src.main import fastapi_app


class MockDatabase(Database):
    async def drop_database(self) -> None:
        if self._engine:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def mock_database() -> AsyncGenerator[MockDatabase, None]:
    db = MockDatabase(db_url=settings.TEST_DATABASE_URL)
    try:
        yield db
    finally:
        await db.drop_database()
        await db.close()


@pytest.fixture(scope="session")
async def my_app(
    mock_database: MockDatabase,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator[FastAPI, None]:
    app = fastapi_app.create_app()
    app.container.db.override(mock_database)
    yield app
    await AsyncCacheManager.delete(key=CacheTag.APPLICATION_SETTINGS.value)
    app.container.reset_override()


@pytest.fixture(scope="function")
async def test_client(
    my_app: FastAPI,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=my_app),
        base_url="http://test",
        timeout=0,
    ) as client:
        yield client
