import functools
import inspect
import json
from collections.abc import Callable
from typing import Any, TypeVar

from redis import RedisError
from src.core.cache.redis_backend import RedisBackendAsync, RedisBackendSync
from src.core.helpers.json_encoder import CustomJSONEncoder
from src.core.logger import logger

T = TypeVar("T", bound=Callable[..., Any])


class AsyncCacheManager:
    def __init__(self) -> None:
        self._backend: RedisBackendAsync | None = None

    @property
    def backend(self) -> RedisBackendAsync:
        if self._backend is None:
            raise RuntimeError("Cache backend is not initialized.")
        return self._backend

    def init(self, backend: RedisBackendAsync) -> None:
        self._backend = backend

    async def get(self, key: str) -> Any:
        try:
            data = await self.backend.get(key)

            if data is None:
                logger.warning("No data found for key: %s", key)
                return False

            return json.loads(data)
        except json.decoder.JSONDecodeError as e:
            logger.error("Error decoding JSON: %s", e)
            return data
        except RedisError as err:
            logger.error("Cannot get cache data: %s", str(err))
            return False

    async def h_get(self, key: str) -> Any:
        try:
            return await self.backend.h_get(key)
        except RedisError as err:
            logger.error("Cannot hgetall cache data: %s", str(err))
            return False

    async def hm_set(self, key: str, mapping: dict[str, Any]) -> bool:
        try:
            await self.backend.hm_set(key=key, mapping=mapping)
        except RedisError as err:
            logger.error("Cannot set cache data: %s", str(err))
            return False
        return True

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        try:
            await self.backend.set(key, json.dumps(value, cls=CustomJSONEncoder), ttl)
        except RedisError as err:
            logger.error("Cannot set cache data: %s", str(err))
            return False
        return True

    async def delete(self, key: str) -> bool:
        try:
            await self.backend.delete(key)
        except RedisError as err:
            logger.error("Cannot delete cache data: %s", str(err))
            return False
        return True

    async def get_delete(self, key: str) -> Any:
        try:
            data = await self.backend.get_delete(key)
            return json.loads(data) if data else None
        except RedisError as err:
            logger.error("Cannot get delete cache data: %s", str(err))
            return False

    async def update_cache(self, key: str, updated_value: dict[str, Any] | Any) -> bool:
        try:
            await self.set(key, updated_value)
            return True
        except RedisError as err:
            logger.error("Cannot update cache data: %s", str(err))
            return False

    async def update_dict_key(self, cache_key: str, dict_key: str, new_value: Any) -> bool:
        try:
            cached_dict = await self.get(cache_key)
            if not isinstance(cached_dict, dict):
                logger.error("Cached data is not a dictionary.")
                return False
            cached_dict[dict_key] = new_value
            await self.set(cache_key, cached_dict)
            return True
        except RedisError as err:
            logger.error("Cannot update dictionary in cache: %s", str(err))
            return False

    async def update_selected_keys(self, cache_key: str, updated_data: dict[str, Any]) -> bool:
        try:
            cached_dict = await self.get(cache_key)
            if not isinstance(cached_dict, dict):
                logger.error("Cached data is not a dictionary.")
                return False

            cached_dict.update(updated_data)
            await self.set(cache_key, cached_dict)
            return True
        except RedisError as err:
            logger.error("Cannot update selected keys in cache: %s", str(err))
            return False

    def key_maker(self, function: Callable[..., Any], prefix: str) -> str:
        module = inspect.getmodule(function)
        module_name = module.__name__ if module is not None else "unknown_module"
        path = f"{prefix}::{module_name}.{function.__name__}"
        args = ""

        for arg in inspect.signature(function).parameters.values():
            args += arg.name

        if args:
            return f"{path}.{args}"

        return path

    def cached(self, prefix: str, expire_time: int | None = None) -> Callable[[T], T]:
        def decorator(func: T) -> T:
            @functools.wraps(func)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                cache_key = prefix  # self.key_maker(function=func, prefix=prefix)
                cached_result = await self.get(cache_key)
                if cached_result:
                    return cached_result
                result = await func(*args, **kwargs)
                await self.set(cache_key, result, expire_time)
                return result

            return wrapper  # type: ignore

        return decorator


class SyncCacheManager:
    def __init__(self) -> None:
        self._backend: RedisBackendSync | None = None

    @property
    def backend(self) -> RedisBackendSync:
        if self._backend is None:
            raise RuntimeError("Cache backend is not initialized.")
        return self._backend

    def init(self, backend: RedisBackendSync) -> None:
        self._backend = backend

    def get(self, key: str) -> Any:
        try:
            data = self.backend.get(key)

            if data is None:
                logger.warning("No data found for key: %s", key)
                return False

            return json.loads(data)
        except json.decoder.JSONDecodeError as e:
            logger.error("Error decoding JSON: %s", e)
            return data
        except RedisError as err:
            logger.error("Cannot get cache data: %s", str(err))
            return False

    def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        try:
            self.backend.set(key, json.dumps(value, cls=CustomJSONEncoder), ttl)
        except RedisError as err:
            logger.error("Cannot set cache data: %s", str(err))
            return False
        return True


ASYNC_CACHE_MANAGER = AsyncCacheManager()

SYNC_CACHE_MANAGER = SyncCacheManager()
