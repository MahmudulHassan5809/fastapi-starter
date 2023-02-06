from typing import Any, Dict, Optional, List


from src.core.crud_base import CRUDBase
from src.accounts.models import User, UserCreate, UserUpdate
from src.accounts.models import User
from src.core.schemas.common import QueryParam


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, data: UserCreate) -> User:
        create_data = data.dict()
        res = await super().create(create_data)
        return res

    async def list(self, queryParam: QueryParam) -> List[User]:
        res = await super().list(queryParam)
        return res

    async def get_by_id(self, id: int) -> Optional[User]:
        res = await super().get_by_id(id)
        return res

    async def update_by_id(self, instance: User, data: UserUpdate) -> Optional[User]:
        return await super().update_by_id(id, instance, data)
