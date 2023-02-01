from fastapi import APIRouter, Depends
from src.accounts.models import UserCreate, UserRead, UserUpdate
from src.accounts.crud import CRUDUser
from src.accounts.dependencies import get_user_crud

router = APIRouter(prefix="/admin")


@router.post("/users", response_model=UserCreate)
async def create_user(
    data: UserCreate,
    user: CRUDUser = Depends(get_user_crud)
):
    return await user.create(data=data)


@router.get("/users", response_model=list[UserRead])
async def get_user(user: CRUDUser = Depends(get_user_crud)):
    return await user.list()


@router.get("/users/{id}", response_model=UserRead)
async def retrieve_user(id: int, user: CRUDUser = Depends(get_user_crud)):
    return await user.get_by_id(id)

@router.patch("/users/{id}", response_model=UserRead)
async def update_user(
    id: int,
    data: UserUpdate,
    user: CRUDUser = Depends(get_user_crud),
):
    return await user.update_by_id(id, data)