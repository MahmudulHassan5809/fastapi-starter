from fastapi import HTTPException, Request

from src.core.cache import Cache, CacheTag
from src.core.permissions.enums import UserGroup
from src.modules.users.models import User


async def get_current_user(request: Request) -> User:
    user_id = request.state.user["user_id"]  # Retrieve user_id from request.state.user
    user_data_key = CacheTag.USER_DATA.value.format(user_id=user_id)
    data = await Cache.get(key=user_data_key)
    if data is None:
        raise HTTPException(status_code=404, detail="User not found")

    data["group"] = UserGroup(data["group"]) if data.get("group") else None

    user = User(**data)
    return user
