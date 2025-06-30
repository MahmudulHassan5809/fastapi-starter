import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import Row
from src.core.models import BaseModel as SqlBaseModel

T = TypeVar("T")


class CustomJSONEncoder(Generic[T], json.JSONEncoder):  # noqa
    def default(self, o: T) -> str | dict[str, Any]:
        if isinstance(o, datetime | date):
            return o.isoformat()
        if isinstance(o, Decimal | bool):
            return str(o)
        if isinstance(o, SqlBaseModel):
            return o.to_dict()
        if isinstance(o, BaseModel):
            return o.model_dump()
        if isinstance(o, Row):
            return o._asdict()

        return str(super().default(o))
