from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db_session import get_session
from src.accounts.crud import CRUDUser
from src.accounts.models import User
from src.accounts.services import UserService


async def get_user_crud(
        session: AsyncSession = Depends(get_session)
) -> CRUDUser:
    return CRUDUser(model=User, session=session)


async def get_user_service(
        user_crud: CRUDUser = Depends(get_user_crud)
) -> UserService:

    return UserService(user_crud=user_crud)
