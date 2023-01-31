from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.crud_base import CRUDBase
from src.accounts.models import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
    #     return db.query(User).filter(User.email == email).first()

    # def update(
    #     self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> User:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)

    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def is_superuser(self, user: User) -> bool:
    #     return user.is_superuser

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        res = await super().create(db, create_data)
        return res
