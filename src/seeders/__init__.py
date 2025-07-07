import asyncio
from src.core.db import Database
from src.core.config import settings
from src.seeders.user_data import seed_user_data


async def seed_all_tables(db: Database) -> None:
    async with db.session() as session:
        await seed_user_data(session=session)
        await session.commit()


async def main() -> None:
    db = Database(db_url=settings.DATABASE_URL)
    await seed_all_tables(db=db)
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())