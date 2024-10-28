import asyncio

from sqlalchemy import text

from src.core.config import settings
from src.core.db import Base, Database
from src.core.error.exceptions import DatabaseError
from src.seeders.users import seed_user_data


class SeedDatabase(Database):
    async def drop_database(self) -> None:
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            result = await connection.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
            )
            tables = [row[0] for row in result.fetchall()]

            # Drop each table with CASCADE
            for table in tables:
                await connection.execute(
                    text(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                )

    async def create_database(self) -> None:
        if self._engine is None:
            raise DatabaseError(message="DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)


async def seed_all_tables(db: SeedDatabase) -> None:
    async with db.session() as session:
        await seed_user_data(session=session)


async def main() -> None:
    db = SeedDatabase(db_url=settings.TEST_DATABASE_URL)
    await db.drop_database()
    await db.create_database()
    await seed_all_tables(db=db)
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
