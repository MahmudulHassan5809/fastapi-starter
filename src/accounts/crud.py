from typing import Any, Dict, Optional, List
from fastapi import HTTPException
from fastapi import status as http_status


from src.core.crud_base import CRUDBase
from src.accounts.models import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, data: UserCreate) -> User:
        create_data = data.dict()
        res = await super().create(create_data)
        return res
    
    async def list(self) -> List[User]:
        res = await super().list()
        return res
    
    async def get_by_id(self, id: int) -> Optional[User]:
        res = await super().get_by_id(id)
        if not res:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )
        return res
    
    async def update_by_id(self, id: int, data: UserUpdate) -> Optional[User]:
        print('---------------------------')
        instance = await self.get_by_id(id)
        return await super().update_by_id(id, instance, data)