# pylint: disable=not-callable
from collections.abc import Callable
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from ulid import ULID

from src.core.db import ModelType
from src.core.db.connector import Base
from src.core.repository import BaseRepository


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(26), primary_key=True, default=lambda: str(ULID())
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False
    )

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for field in self.__table__.c:
            value = getattr(self, field.name)

            if isinstance(value, (Decimal, bool)):
                result[field.name] = str(value)
            elif isinstance(value, (date, time, datetime)):
                result[field.name] = value.isoformat()
            else:
                result[field.name] = value

        return result

    @classmethod
    def objects(
        cls: type[ModelType], session_factory: Callable[[], AsyncSession]
    ) -> BaseRepository[ModelType]:
        return BaseRepository(cls, session_factory)
