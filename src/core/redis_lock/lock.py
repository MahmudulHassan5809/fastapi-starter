import uuid
from typing import Any

import redis.asyncio as redis
from redis import Redis
from src.core.error.codes import LOCK_ERROR
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import ERROR_MAPPER


class RedisTransactionAsyncLock:
    def __init__(self, user_ids: list[str], url: str, ttl: int = 30) -> None:
        self.user_ids = user_ids
        self.locks: dict[str, Any] = {}
        self.ttl = ttl
        self.lock_value = str(uuid.uuid4())
        self.redis_client: redis.Redis = redis.from_url(url=url, decode_responses=True)

    async def acquire(self) -> bool:
        """Attempt to acquire locks for all user IDs."""
        import time

        time.sleep(0.05)  # Simulate a delay for testing purposes
        for user_id in self.user_ids:
            lock_key = f"user:{user_id}:lock"
            lock_value = str(uuid.uuid4())
            acquired = await self.redis_client.set(lock_key, lock_value, nx=True, ex=self.ttl)
            if not acquired:
                await self.release()
                return False
            self.locks[lock_key] = lock_value
        return True

    async def release(self) -> None:
        async with self.redis_client.pipeline() as pipe:
            for lock_key, lock_value in self.locks.items():
                current_value = await self.redis_client.get(lock_key)
                if current_value == lock_value:
                    pipe.multi()
                    pipe.delete(lock_key)
                    await pipe.execute()
            await pipe.unwatch()
        self.locks.clear()

    async def __aenter__(self) -> "RedisTransactionAsyncLock":
        acquired = await self.acquire()
        if not acquired:
            raise ValidationException(errors=ERROR_MAPPER[LOCK_ERROR])
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        await self.release()
        await self.redis_client.close()


class RedisTransactionSyncLock:
    def __init__(self, user_ids: list[str], url: str, ttl: int = 30) -> None:
        self.user_ids = user_ids
        self.locks: dict[str, Any] = {}
        self.ttl = ttl
        self.lock_value = str(uuid.uuid4())
        self.redis_client: Redis = Redis.from_url(url=url, decode_responses=True)

    def acquire(self) -> bool:
        """Attempt to acquire locks for all user IDs."""
        import time

        time.sleep(0.05)
        for user_id in self.user_ids:
            lock_key = f"user:{user_id}:lock"
            lock_value = str(uuid.uuid4())
            acquired = self.redis_client.set(lock_key, lock_value, nx=True, ex=self.ttl)
            if not acquired:
                self.release()
                return False
            self.locks[lock_key] = lock_value
        return True

    def release(self) -> None:
        pipe = self.redis_client.pipeline()
        try:
            for lock_key, lock_value in self.locks.items():
                current_value = self.redis_client.get(lock_key)
                if current_value == lock_value:
                    pipe.delete(lock_key)
            pipe.execute()
        finally:
            self.locks.clear()

    def __enter__(self) -> "RedisTransactionSyncLock":
        acquired = self.acquire()
        if not acquired:
            raise ValidationException(errors=ERROR_MAPPER[LOCK_ERROR])
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.release()
        self.redis_client.close()
