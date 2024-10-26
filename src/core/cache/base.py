from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Any


class AbstractRedisBackend(ABC):

    @abstractmethod
    async def get(self, key: str) -> Any:
        pass

    @abstractmethod
    async def h_get(self, key: str) -> Awaitable[dict[Any, Any]] | dict[Any, Any]:
        pass

    @abstractmethod
    async def get_delete(self, key: str) -> Any:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire_time: int | None = None) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
