from src.accounts.models import UserCreate, UserUpdate
from src.accounts.crud import CRUDUser
from src.core.schemas.common import QueryParam
from fastapi import HTTPException
from fastapi import status as http_status

class UserService():
    def __init__(self, user_crud: CRUDUser):
        self.crud = user_crud

    async def create_user(self, data: UserCreate):
        return await self.crud.create(data)
    
    async def user_list(self, queryParam: QueryParam):
        return await self.crud.list(queryParam)

    async def get_single_user(self, user_id: int):
        res = await self.crud.get_by_id(user_id)
        if not res:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )
        return res
    
    async def update_user(self, id: int, data: UserUpdate):
        instance = await self.get_single_user(id)
        return await self.crud.update_by_id(instance, data)