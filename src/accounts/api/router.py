from fastapi import APIRouter, Depends

from src.accounts.api.admin_controller import router as admin_router
from src.accounts.api.auth_controller import router as auth_router

from src.core.dependencies.auth_dependency import JWTBearer

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (admin_router, "accounts", "Admin Accounts", "private"),
    (auth_router, "authentication", "Accounts Authentication", "public"),
)

for router_item in routers:
	router, prefix, tag, api_type = router_item

	if api_type == "private":
		include_api(router, prefix=f"/{prefix}", tags=[tag], dependencies=[Depends(JWTBearer())]) 
	else:
		include_api(router, prefix=f"/{prefix}", tags=[tag],)
	