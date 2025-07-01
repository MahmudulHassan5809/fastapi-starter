import functools
import time
from collections.abc import Callable
from typing import Any

import redis.asyncio as redis
from fastapi import Request
from redis import Redis
from src.core.config import settings
from src.core.error.codes import INTERNAL_ERROR, TOO_MANY_REQUEST
from src.core.error.exceptions import ValidationException
from src.core.error.format_error import ERROR_MAPPER
from src.core.logger import logger


class RateLimiter:
    def __init__(self) -> None:
        self.redis_pool: redis.ConnectionPool = redis.ConnectionPool.from_url(settings.REDIS_URL)

    def get_redis(self) -> Redis:
        return redis.Redis(connection_pool=self.redis_pool)

    async def is_rate_limited(self, key: str, max_requests: int, window: int) -> bool:
        current = int(time.time())
        window_start = current - window
        redis_conn = self.get_redis()
        async with redis_conn.pipeline() as pipe:
            try:
                await pipe.zremrangebyscore(key, 0, window_start)
                await pipe.zcard(key)
                await pipe.zadd(key, {str(current).encode("utf-8"): float(current)})
                await pipe.expire(key, window)
                results = await pipe.execute()
            except redis.RedisError as e:
                logger.error("RateLimit error : %s", str(e))
                raise ValidationException(errors=ERROR_MAPPER[INTERNAL_ERROR]) from e
        return results[1] >= max_requests  # type: ignore

    def rate_limit(self, max_requests: int, window: int) -> Callable[[Any], Any]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
                if request.headers.get("X-Forwarded-For"):
                    client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0]
                else:
                    client_ip = request.client.host if request.client else "no_host"
                key = f"rate_limit:{client_ip}:{request.url.path}"
                if await self.is_rate_limited(key, max_requests, window):
                    raise ValidationException(errors=ERROR_MAPPER.get(TOO_MANY_REQUEST))
                return await func(request, *args, **kwargs)

            return wrapper

        return decorator


RateLimit = RateLimiter()
