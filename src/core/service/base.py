from math import ceil

from src.core.schemas.common import PaginationMeta


class BaseService:
    async def setup_pagination_meta(self, total: int, page_size: int, page: int) -> PaginationMeta:
        last_page = ceil(total / page_size)
        next_page = page + 1 if page < last_page else None
        prev_page = page - 1 if page > 1 else None

        return PaginationMeta(
            total=total,
            current_page=page,
            next_page=next_page,
            prev_page=prev_page,
            last_page=last_page,
        )
