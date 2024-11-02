from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import PasswordHandler
from src.modules.users.models import User


async def seed_user_data(session: AsyncSession) -> None:
    user_data = [
        User(
            name="Mahmudul Hassan",
            phone="01630811624",
            gender="MALE",
            password=PasswordHandler.hash("123456"),
            email="johndoe@example.com",
            status="ACTIVE",
            dob="1994-04-07",
        ),
        User(
            name="Jane Doe",
            phone="01630811623",
            gender="FEMALE",
            password=PasswordHandler.hash("123456"),
            email="janedoe@example.com",
            status="ACTIVE",
            dob="1994-04-07",
        ),
    ]

    session.add_all(user_data)
    await session.commit()
