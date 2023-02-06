from fastapi import APIRouter, Depends

from src.accounts.api.admin_controller import router as admin_router
from src.accounts.api.auth_controller import router as auth_router

from src.core.dependencies.auth_dependency import JWTBearer

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (admin_router, "accounts", "Admin Accounts"),
    (auth_router, "authentication", "Accounts Authentication"),
)

for router_item in routers:
   router, prefix, tag = router_item
   include_api(router, prefix=f"/{prefix}", tags=[tag],) #  dependencies=[Depends(JWTBearer())],
