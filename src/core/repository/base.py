# pylint: disable=not-callable
from collections.abc import Callable, Sequence
from typing import Any, Generic

from sqlalchemy import (
    JSON,
    RowMapping,
    Select,
    and_,
    cast,
    func,
    or_,
    select,
    text,
    update,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty, joinedload, selectinload
from src.core.db import ModelType, operators_map
from src.core.schemas.common import FilterOptions


class BaseRepository(Generic[ModelType]):  # noqa
    def __init__(self, model: type[ModelType], session_factory: Callable[[], AsyncSession]):
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
            # options.extend(joinedload(getattr(self.model, x)) for x in prefetch)
            for relation in prefetch:
                attr = getattr(self.model, relation)
                # Use selectinload for one-to-many, joinedload for one-to-one
                if isinstance(attr.property, RelationshipProperty) and attr.property.uselist:
                    options.append(selectinload(attr))  # One-to-many
                else:
                    options.append(joinedload(attr))  # One-to-one
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

    # def _build_filters(self, filters: dict[str, Any]) -> list[Any]:
    #     """Build list of WHERE conditions."""
    #     result = []
    #     for expression, value in filters.items():
    #         parts = expression.split("__")
    #         op_name = parts[1] if len(parts) > 1 else "exact"

    #         if op_name not in operators_map:
    #             raise KeyError(
    #                 f"Expression {expression} has incorrect operator {op_name}"
    #             )

    #         operator = operators_map[op_name]
    #         column = getattr(self.model, parts[0])

    #         if isinstance(value, dict) and isinstance(column.type, JSON):
    #             for json_key, json_value in value.items():
    #                 json_path = column[json_key]  # Access JSON field
    #                 result.append(operator(json_path, json_value))
    #         else:
    #             result.append(operator(column, value))

    #     return result

    async def filter(
        self,
        filter_options: FilterOptions,
    ) -> Sequence[ModelType]:
        query = self._get_query(filter_options.prefetch)

        if filter_options.distinct_on:
            query = query.distinct(getattr(self.model, filter_options.distinct_on))
        if filter_options.sorting is not None:
            query = query.order_by(*self._build_sorting(filter_options.sorting))

        condition = (
            or_(*self._build_filters(filter_options.filters))
            if filter_options.use_or
            else and_(*self._build_filters(filter_options.filters))
        )
        async with self.session() as session:
            db_execute = await session.execute(query.where(condition))
            return db_execute.scalars().all()

    async def paginate_filter(  # pylint: disable=too-many-locals, too-many-branches
        self,
        filter_options: FilterOptions,
    ) -> tuple[Sequence[ModelType], int]:
        query = self._get_query(filter_options.prefetch)

        if filter_options.sorting is not None:
            query = query.order_by(*self._build_sorting(filter_options.sorting))

        filters = self._build_filters(filter_options.filters)

        or_conditions = []
        and_conditions = []
        search_conditions = []

        search_fields = filter_options.search_fields

        if filter_options.pagination and filter_options.pagination.search and search_fields:
            search_value = filter_options.pagination.search.strip()
            for field in search_fields:
                search_conditions.append(getattr(self.model, field).ilike(f"%{search_value}%"))

        for filter_expr in filters:
            if hasattr(filter_expr, "left") and hasattr(filter_expr.left, "key"):
                if (
                    filter_options.or_filters is not None
                    and filter_expr.left.key in filter_options.or_filters
                ):
                    or_conditions.append(filter_expr)
                else:
                    and_conditions.append(filter_expr)

        final_condition = None
        if and_conditions or or_conditions or search_conditions:
            combined_conditions = []
            if and_conditions:
                combined_conditions.append(and_(*and_conditions))
            if or_conditions:
                combined_conditions.append(or_(*or_conditions))
            if search_conditions:
                combined_conditions.append(or_(*search_conditions))

            final_condition = and_(*combined_conditions) if combined_conditions else None
        async with self.session() as session:
            total_query = select(func.count()).select_from(self.model)
            if final_condition is not None:
                total_query = total_query.where(final_condition)
            total = await session.scalar(total_query) or 0

            # Apply pagination if provided
            if filter_options.pagination:
                query = query.offset(filter_options.pagination.skip).limit(
                    filter_options.pagination.page_size
                )

            if final_condition is not None:
                query = query.where(final_condition)
            db_execute = await session.execute(query)
            result = db_execute.scalars().all()

        return result, total

    async def paginate_raw_filter(
        self,
        filter_options: FilterOptions,
    ) -> tuple[Sequence[dict[str, Any]], int]:
        async with self.session() as session:
            total_query = f"""
            SELECT COUNT(*) AS total_count
            FROM ({filter_options.raw_query}) AS subquery
            """
            total_result = await session.execute(text(total_query), filter_options.filters)
            total = total_result.scalar() or 0

            paginated_query = f"""
            {filter_options.raw_query}
            LIMIT :limit OFFSET :offset
            """
            filter_options.filters.update(
                {
                    "limit": (
                        filter_options.pagination.page_size if filter_options.pagination else 1
                    ),
                    "offset": (filter_options.pagination.skip if filter_options.pagination else 10),
                }
            )
            result = await session.execute(text(paginated_query), filter_options.filters)

            # Fetch all results
            data = [u._asdict() for u in result]

        return data, total

    async def get_by_id(
        self, obj_id: str, prefetch: tuple[str, ...] | None = None
    ) -> ModelType | None:
        query = self._get_query(prefetch).where(self.model.id == obj_id)  # type: ignore

        async with self.session() as session:
            result_cursor = await session.execute(query)
            return result_cursor.scalars().first()

    async def get_by_field(
        self,
        filter_options: FilterOptions,
    ) -> ModelType | None:
        query = self._get_query(filter_options.prefetch)

        if filter_options.distinct_on:
            query = query.distinct(getattr(self.model, filter_options.distinct_on))
        if filter_options.sorting is not None:
            query = query.order_by(*self._build_sorting(filter_options.sorting))

        or_conditions = []
        and_conditions = []

        filters = self._build_filters(filter_options.filters)

        for filter_expr in filters:
            if hasattr(filter_expr, "left") and hasattr(filter_expr.left, "key"):
                if (
                    filter_options.or_filters is not None
                    and filter_expr.left.key in filter_options.or_filters
                ):
                    or_conditions.append(filter_expr)
                else:
                    and_conditions.append(filter_expr)

        final_condition = None
        if and_conditions or or_conditions:
            combined_conditions = []
            if and_conditions:
                combined_conditions.append(and_(*and_conditions))
            if or_conditions:
                combined_conditions.append(or_(*or_conditions))
            final_condition = and_(*combined_conditions) if combined_conditions else None
        async with self.session() as session:
            db_execute = await session.execute(query.where(final_condition))  # type: ignore
            return db_execute.scalars().first()

    async def get_first(self) -> ModelType | None:
        async with self.session() as session:
            result_cursor = await session.execute(select(self.model))
            return result_cursor.scalars().first()

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

    async def get_raw_all(
        self, sql: str, query: dict[str, Any] | None = None
    ) -> Sequence[RowMapping]:
        stmt = text(sql)
        async with self.session() as session:
            result_cursor = await session.execute(stmt, query)
            return result_cursor.mappings().all()

    async def count(self, filters: dict[str, Any]) -> int:
        query = select(func.count()).select_from(self.model)

        query = query.where(and_(True, *self._build_filters(filters)))
        async with self.session() as session:
            result_cursor = await session.execute(query)
            result = result_cursor.scalars().first()
        return result if result else 0

    async def update(self, where: dict[str, Any], values: dict[str, Any]) -> int:
        async with self.session() as session:
            filters = self._build_filters(where)

            # Convert column names to strings for `values`
            update_values = {}
            for key, value in values.items():
                if isinstance(value, dict) and isinstance(getattr(self.model, key).type, JSON):
                    update_values[key] = cast(getattr(self.model, key), JSONB).concat(
                        cast(value, JSONB)
                    )
                else:
                    update_values[key] = value

            query = update(self.model).where(and_(True, *filters)).values(**update_values)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount

    async def create_or_update(
        self,
        where: dict[str, Any],
        values: dict[str, Any],
    ) -> ModelType:
        async with self.session() as session:
            filters = self._build_filters(where)
            query = select(self.model).where(and_(*filters))

            existing_obj = await session.execute(query)
            existing_obj = existing_obj.scalars().first()  # type: ignore

            if existing_obj:
                for key, value in values.items():
                    setattr(existing_obj, key, value)
                session.add(existing_obj)
                await session.commit()
                await session.refresh(existing_obj)
                return existing_obj  # type: ignore

            new_obj = self.model(**values)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
            return new_obj

    async def get_all(
        self,
        prefetch: tuple[str, ...] | None = None,
        sorting: dict[str, str] | None = None,
    ) -> Sequence[ModelType]:
        query = self._get_query(prefetch)

        if sorting is not None:
            query = query.order_by(*self._build_sorting(sorting))

        async with self.session() as session:
            result_cursor = await session.execute(query)
            return result_cursor.scalars().all()
