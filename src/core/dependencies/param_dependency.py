from typing import Union
from fastapi import Request
from src.core.schemas.common import QueryParam

async def common_parameters(
    request:Request,
    q: Union[str, None] = None, 
    page: int = 1, limit: int = 10,
    ) -> QueryParam:
    data = {"search": q, "page": page, "limit": limit}

    query_clone = dict(request.query_params).copy()
    entries_to_remove = ('page', 'number', 'search')
    for k in entries_to_remove:
        query_clone.pop(k, None)
    
    data['filter'] = query_clone
    
    return QueryParam(**data)


class CommonParam():
    def __init__(self, filter_fields:list):
        self.filter_fields = filter_fields
    
    def __call__(self, request:Request, search: Union[str, None] = None,  page: int = 1, limit: int = 10)-> QueryParam:
        data = {"search": search, "page": page, "limit": limit if limit > 0 else None, "offset_limit": limit}

        query_clone = dict(request.query_params).copy()
        entries_to_remove = ('page', 'number', 'search')
        for k in entries_to_remove:
            query_clone.pop(k, None)
        
        query_clone = dict((k,v) for k,v in query_clone.items() if k in self.filter_fields)
        data['filter'] = query_clone
        return QueryParam(**data)