from fastapi import APIRouter, Depends

from src.core.dependencies.authentication import JWTBearer
from src.modules.users.controllers import user_admin_router, user_router

api_router = APIRouter()
include_api = api_router.include_router


routers = (
    (user_router, "users", "User Private Route", "private"),
    (user_admin_router, "admin/users", "User Admin Private Route", "private"),
)

for router_item in routers:
    router, prefix, tag, api_type = router_item

    if api_type == "private":
        include_api(
            router,
            prefix=f"/{prefix}",
            tags=[tag],
            dependencies=[Depends(JWTBearer())],
        )
    else:
        include_api(
            router,
            prefix=f"/{prefix}",
            tags=[tag],
        )
