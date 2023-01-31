from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


engine = create_async_engine(settings.DATABASE_URI, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False,)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
