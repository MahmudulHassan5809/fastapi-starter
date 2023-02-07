from fastapi import HTTPException
from fastapi import status as http_status


from src.accounts.models import UserCreate, UserUpdate
from src.accounts.crud import CRUDUser
from src.accounts.utils import verify, hash
from src.accounts.oauth2 import create_access_token, create_refresh_token
from src.accounts.schemas import Token
from src.core.schemas.common import QueryParam

class UserService():
    def __init__(self, user_crud: CRUDUser):
        self.crud = user_crud

    async def create_user(self, data: UserCreate):
        res = await self.crud.get('username', data.username)
        if  res:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        hashed_password = hash(data.password)
        data.password = hashed_password
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
    
    async def login(self, user_credentials: any) -> Token:
        res = await self.crud.get('username', user_credentials.username)
        if not res:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        if not verify(user_credentials.password, res.password):
            raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        

        access_token = create_access_token(data = {"user_id" : res.id})
        refresh_token = create_refresh_token(data = {"user_id" : res.id})
        return {"access_token" : access_token, "refresh_token": refresh_token}
    
    async def update_user(self, id: int, data: UserUpdate):
        instance = await self.get_single_user(id)
        return await self.crud.update_by_id(instance, data)