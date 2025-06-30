from typing import Any

import redis as sync_redis
import redis.asyncio as redis


class RedisBackendAsync:
    def __init__(self, url: str):
        self.redis_client: redis.Redis = redis.from_url(url=url, decode_responses=True)

    async def get(self, key: str) -> Any:
        return await self.redis_client.get(key)

    async def h_get(self, key: str) -> Any:
        return await self.redis_client.hgetall(key)

    async def hm_set(self, key: str, mapping: dict[str, Any]) -> None:
        await self.redis_client.hmset(key, mapping)

    async def get_delete(self, key: str) -> Any:
        return await self.redis_client.getdel(key)

    async def set(self, key: str, value: Any, expire_time: int | None = None) -> None:
        if expire_time:
            await self.redis_client.setex(key, expire_time, value)
        else:
            await self.redis_client.set(key, value)

    async def delete(self, key: str) -> None:
        await self.redis_client.delete(key)


class RedisBackendSync:
    def __init__(self, url: str):
        self.redis_client: sync_redis.Redis = sync_redis.StrictRedis.from_url(
            url, decode_responses=True
        )

    def get(self, key: str) -> Any:
        return self.redis_client.get(key)

    def set(self, key: str, value: Any, expire_time: int | None = None) -> None:
        if expire_time:
            self.redis_client.setex(key, expire_time, value)
        else:
            self.redis_client.set(key, value)
