from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager

import psycopg
from psycopg.rows import dict_row
from src.core.config import settings
from src.core.error.exceptions import DatabaseError


@contextmanager
def get_conn() -> Generator[psycopg.Connection, None, None]:
    conn = None
    try:
        conn = psycopg.connect(
            settings.DATABASE_URL.replace("postgresql+psycopg://", "postgresql://"),
            row_factory=dict_row,
        )
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise DatabaseError from e
    finally:
        if conn:
            conn.close()  # pylint: disable=no-member


@asynccontextmanager
async def get_async_conn() -> AsyncGenerator[psycopg.AsyncConnection, None]:
    conn = None
    try:
        conn = await psycopg.AsyncConnection.connect(
            settings.DATABASE_URL.replace("postgresql+psycopg://", "postgresql://"),
            row_factory=dict_row,
        )
        yield conn
    except Exception as e:
        if conn:
            await conn.rollback()
        raise DatabaseError from e
    finally:
        if conn:
            await conn.close()
