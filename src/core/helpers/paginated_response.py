import math
from typing import List, Optional


def paginateResponse(data : List, total : Optional[int], page : Optional[int], limit: Optional[int]):
    lastPage = math.ceil(total / limit) if limit > 0 else  1
    nextPage = None if page + 1 > lastPage else page + 1
    prevPage = None if page - 1 < 1 > lastPage else page - 1
    return {
        'data': data,
        'meta_info': {
            'count': total,
            'currentPage': page,
            'nextPage': nextPage,
            'prevPage': prevPage,
            'lastPage': lastPage if lastPage > 0 else page,
        }
    }