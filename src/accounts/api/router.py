from fastapi import APIRouter

from src.accounts.api.admin_controller import router as admin_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (admin_router, "accounts", "Admin Accounts"),
)

for router_item in routers:
   router, prefix, tag = router_item
   include_api(router, prefix=f"/{prefix}", tags=[tag])
