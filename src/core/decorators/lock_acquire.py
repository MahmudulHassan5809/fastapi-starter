from collections.abc import Callable
from functools import wraps
from typing import Any, TypeGuard

from src.core.config import settings
from src.core.redis_lock import RedisTransactionAsyncLock


def is_str(value: str | None) -> TypeGuard[str]:
    return isinstance(value, str)


def acquire_lock(
    user_id_param: str = "user_id",
    receiver_id_param: str | None = None,
) -> Callable[..., Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            user_id = kwargs.get(user_id_param)
            if not user_id:
                raise ValueError(f"{user_id_param} is required for acquire_lock decorator")
            user_ids = [user_id]
            if receiver_id_param:
                receiver_id = kwargs.get(receiver_id_param)
                if receiver_id:
                    user_ids.append(receiver_id)

            async with RedisTransactionAsyncLock(user_ids=user_ids, url=settings.REDIS_URL):
                return await func(*args, **kwargs)

        return wrapper

    return decorator
