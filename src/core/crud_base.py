from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.schemas.common import QueryParam
from src.core.helpers.paginated_response import paginateResponse

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        statement = select(self.model).where(self.model.id == id)
        results = await self.session.execute(statement=statement)
        return results.scalar_one_or_none()
    

    async def get(self, filter_field: any, filter_value: any) -> Optional[ModelType]:
        filter_field = getattr(self.model, filter_field)
        statement = select(self.model).where(filter_field == filter_value)
        results = await self.session.execute(statement=statement)
        return results.scalar_one_or_none()


    async def list(self, queryParam: QueryParam) -> List[ModelType]:
        offset = (queryParam.page - 1) * queryParam.offset_limit
        limit = queryParam.limit
        
        filters = []
        for key, value in queryParam.filter.items():
            filters.append(getattr(self.model, key) == value)
        
        print(filters)

        data = await self.session.execute(
            select(self.model)
            .where(*filters)
            .offset(offset)
            .limit(limit)
        )

        data = data.scalars().all()
        return paginateResponse(data, 1, queryParam.page, queryParam.offset_limit)



    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def update_by_id(self, id: int, instance: Type[ModelType], obj_in: UpdateSchemaType):
        data = obj_in.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(instance, key, value)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance
