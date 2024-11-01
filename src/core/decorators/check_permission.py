from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from fastapi import Depends, HTTPException, status

from src.core.dependencies.get_current_user import get_current_user
from src.core.permissions.acl import ACL
from src.core.permissions.enums import UserPermission
from src.modules.users.models import User


def check_permission(
    permission: UserPermission,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        @wraps(func)
        async def wrapper(
            *args: Any, user: User = Depends(get_current_user), **kwargs: Any
        ) -> Any:
            acl = ACL(user.__acl__())
            if user.is_superuser:
                return await func(*args, user=user, **kwargs)

            if not user.group or not acl.is_allowed(
                user.group.value, user.id, permission
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions.",
                )
            return await func(*args, user=user, **kwargs)

        return wrapper

    return decorator
