from fastapi import APIRouter, Depends
from src.accounts.models import UserCreate, UserRead, UserUpdate
from src.accounts.services import UserService
from src.accounts.dependencies import get_user_service
from src.core.schemas.common import PaginatedResponse
from src.core.dependencies.param_dependency import CommonParam

router = APIRouter(prefix="/admin")


@router.post("/users", response_model=UserCreate)
async def create_user(
    data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(data=data)


@router.get("/users", response_model=PaginatedResponse[UserRead])
async def get_user(
    user_service: UserService = Depends(get_user_service),
    commons: dict = Depends(CommonParam(filter_fields=["name"]))
):
    return await user_service.user_list(commons)


@router.get("/users/{id}", response_model=UserRead)
async def retrieve_user(id: int, user_service: UserService = Depends(get_user_service)):
    return await user_service.get_single_user(id)

@router.patch("/users/{id}", response_model=UserRead)
async def update_user(
    id: int,
    data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user(id, data)