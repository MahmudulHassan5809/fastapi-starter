from typing import Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel
from pydantic.generics import GenericModel


Model = TypeVar("Model", bound=BaseModel)

class QueryParam(BaseModel):
    search: Union[str, None] = None
    page: int
    limit: Union[str, None]
    offset_limit: int
    filter: Optional[dict]

    class Config:
        orm_mode = True


class PaginatedResponse(GenericModel, Generic[Model]):
    data : List[Model]
    meta_info: dict = {}