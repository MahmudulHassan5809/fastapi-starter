import os, sys, inspect
import logging
import asyncio



current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)

from src.core.helpers.type_choices import UserStatusType
from src.accounts.models import User
from src.accounts.utils import hash
from src.db.db_session import async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPER_USER_DATA = {
    "name": "Mahmudul Hassan",
    "email": "admin@gmail.com",
    "username": "admin",
    "phone_number": "0163081624",
    "is_superuser": True,
    "is_staff": True,
    "type": UserStatusType.SUPER_ADMIN,
    "password": hash("123456")
}

async def create_user() -> None:
    async with async_session() as session:
        # # Try to create session to check if DB is awake
        # await session.execute("SELECT 1")
        db_obj = User(**SUPER_USER_DATA)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)


def main() -> None:
    logger.info("Initializing service")
    asyncio.run(create_user())
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()