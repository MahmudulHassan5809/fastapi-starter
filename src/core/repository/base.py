# pylint: disable=not-callable
from collections.abc import Callable, Sequence
from typing import Any, Generic

from sqlalchemy import Select, and_, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.db import ModelType, operators_map
from src.core.schemas.common import PaginationParams


class BaseRepository(Generic[ModelType]):
    def __init__(
        self, model: type[ModelType], session_factory: Callable[[], AsyncSession]
    ):
        self.session = session_factory
        self.model: type[ModelType] = model

    def _get_query(
        self,
        prefetch: tuple[str, ...] | None = None,
        options: list[Any] | None = None,
    ) -> Select[tuple[ModelType]]:
        query = select(self.model)
        if prefetch:
            if not options:
                options = []
            options.extend(joinedload(getattr(self.model, x)) for x in prefetch)
            query = query.options(*options).execution_options(populate_existing=True)
        return query

    def _build_sorting(self, sorting: dict[str, str]) -> list[Any]:
        """Build list of ORDER_BY clauses."""
        result = []
        for field_name, direction in sorting.items():
            field = getattr(self.model, field_name)
            result.append(getattr(field, direction)())
        return result

    def _build_filters(self, filters: dict[str, Any]) -> list[Any]:
        """Build list of WHERE conditions."""
        result = []
        for expression, value in filters.items():
            parts = expression.split("__")
            op_name = parts[1] if len(parts) > 1 else "exact"
            if op_name not in operators_map:
                msg = f"Expression {expression} has incorrect operator {op_name}"
                raise KeyError(msg)
            operator = operators_map[op_name]
            column = getattr(self.model, parts[0])
            result.append(operator(column, value))
        return result

    async def filter(
        self,
        filters: dict[str, Any],
        sorting: dict[str, str] | None = None,
        prefetch: tuple[str, ...] | None = None,
        use_or: bool = False,
    ) -> Sequence[ModelType]:
        query = self._get_query(prefetch)
        if sorting is not None:
            query = query.order_by(*self._build_sorting(sorting))

        condition = (
            or_(*self._build_filters(filters))
            if use_or
            else and_(*self._build_filters(filters))
        )
        async with self.session() as session:
            db_execute = await session.execute(query.where(condition))
            result = db_execute.scalars().all()
        return result

    async def paginate_filter(
        self,
        filters: dict[str, Any],
        pagination: PaginationParams | None = None,
        sorting: dict[str, str] | None = None,
        prefetch: tuple[str, ...] | None = None,
        use_or: bool = False,
    ) -> tuple[Sequence[ModelType], int]:
        query = self._get_query(prefetch)
        if sorting is not None:
            query = query.order_by(*self._build_sorting(sorting))

        condition = (
            or_(*self._build_filters(filters))
            if use_or
            else and_(*self._build_filters(filters))
        )

        async with self.session() as session:
            total_query = select(func.count()).select_from(
                query.where(condition).subquery()
            )
            total = await session.scalar(total_query) or 0

            # Apply pagination if provided
            if pagination:
                query = query.offset(pagination.skip).limit(pagination.page_size)

            db_execute = await session.execute(query.where(condition))
            result = db_execute.scalars().all()

        return result, total

    async def get_by_id(
        self, obj_id: str, prefetch: tuple[str, ...] | None = None
    ) -> ModelType | None:
        query = self._get_query(prefetch).where(self.model.id == obj_id)  # type: ignore
        async with self.session() as session:
            result_cursor = await session.execute(query)
            result = result_cursor.scalars().first()
        return result

    async def get_by_field(
        self,
        filters: dict[str, Any],
        sorting: dict[str, str] | None = None,
        prefetch: tuple[str, ...] | None = None,
        use_or: bool = False,
    ) -> ModelType | None:
        query = self._get_query(prefetch)
        async with self.session() as session:
            if sorting is not None:
                query = query.order_by(*self._build_sorting(sorting))

            condition = (
                or_(*self._build_filters(filters))
                if use_or
                else and_(*self._build_filters(filters))
            )
            result_cursor = await session.execute(query.where(condition))
            result = result_cursor.scalars().first()

        return result

    async def get_first(self) -> ModelType | None:
        async with self.session() as session:
            result_cursor = await session.execute(select(self.model))
            result = result_cursor.scalars().first()
        return result

    async def create(self, obj: ModelType) -> ModelType:
        async with self.session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj

    async def raw_get_one(
        self, sql: str, query: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        stmt = text(sql)
        async with self.session() as session:
            result_cursor = await session.execute(stmt, query)
            result = result_cursor.first()
        return result._as_dict() if result else None  # pylint: disable=protected-access

    async def count(self, filters: dict[str, Any]) -> int:
        query = select(func.count()).select_from(self.model)

        query = query.where(and_(True, *self._build_filters(filters)))
        async with self.session() as session:
            result_cursor = await session.execute(query)
            result = result_cursor.scalars().first()
        return result if result else 0
