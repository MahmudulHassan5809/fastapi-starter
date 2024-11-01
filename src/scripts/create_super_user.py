import asyncio
import os

from sqlalchemy import select

from src.core.db import Database
from src.core.helpers.enums import ProfileStatusEnum
from src.core.logger import logger
from src.core.permissions.enums import UserGroup
from src.core.security import PasswordHandler
from src.modules.users.models import User

# Retrieve database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

db = Database(db_url=DATABASE_URL)


async def create_superuser() -> None:
    email = input("Enter superuser email: ")
    password = input("Enter superuser password: ")
    name = input("Enter first name: ")
    phone = input("Enter phone number: ")
    gender = input("Enter gender: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")

    hashed_password = PasswordHandler.hash(password)

    async with db.session() as session:
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalars().first()
        if existing_user:
            logger.info("A superuser with this email already exists.")
            return

        superuser = User(
            name=name,
            phone=phone,
            gender=gender,
            dob=dob,
            status=ProfileStatusEnum.ACTIVE,
            is_staff=True,
            is_superuser=True,
            email=email,
            last_logged_in_at=None,
            password=hashed_password,
            group=UserGroup.SUPER_ADMIN,
        )

        session.add(superuser)
        await session.commit()
        logger.info("Superuser created successfully!")


# Run the script
if __name__ == "__main__":
    asyncio.run(create_superuser())
