from fastapi import Request

from src.core.schemas.common import QueryParams


class CommonQueryParam:
    def __init__(self, filter_fields: list[str] | None = None):
        self.filter_fields = filter_fields

    def __call__(
        self,
        request: Request,
        search: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> QueryParams:
        data = {
            "search": search,
            "page": page,
            "page_size": page_size,
            "filter_fields": self.filter_fields,
        }

        query_clone = dict(request.query_params).copy()
        entries_to_remove = ("page", "page_size", "search")
        for key in entries_to_remove:
            query_clone.pop(key, None)

        query_clone = {
            k: v for k, v in query_clone.items() if k in (self.filter_fields or [])
        }
        data["filter_params"] = query_clone  # type: ignore

        return QueryParams(**data)
