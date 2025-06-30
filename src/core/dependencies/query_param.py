from typing import Any

from fastapi import Request
from src.core.schemas.common import QueryParams


class CommonQueryParam:
    def __init__(
        self,
        filter_fields: list[str] | None = None,
    ) -> None:
        self.filter_fields = filter_fields
        self.sorting: dict[Any, Any] | None = None

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
            "sorting": self.sorting,
        }

        query_clone = dict(request.query_params).copy()
        entries_to_remove = ("page", "page_size", "search")
        for key in entries_to_remove:
            query_clone.pop(key, None)

        # query_clone = {
        #     k: v for k, v in query_clone.items() if k in (self.filter_fields or [])
        # }

        filter_params = {}
        for key, value in query_clone.items():
            if self.filter_fields and key in self.filter_fields:
                if "," in value:
                    value = value.replace(" ", "")
                    filter_params[f"{key}__in"] = value.split(",")
                else:
                    filter_params[key] = value

        if query_clone.get("order_by_fields"):
            data["sorting"] = {
                query_clone.get("order_by_fields"): query_clone.get("ordering", "desc")
            }

        data["filter_params"] = filter_params

        return QueryParams(**data)
