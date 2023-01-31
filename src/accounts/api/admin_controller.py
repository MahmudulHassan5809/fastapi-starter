from fastapi import APIRouter, Depends
from src.accounts.models import UserCreate
from src.accounts.crud import CRUDUser
from src.accounts.dependencies import get_user_crud

router = APIRouter(
    prefix="/accounts",
    tags=['Accounts']
)


@router.post("/users", response_model=UserCreate)
async def create_user(
    data: UserCreate,
    user: CRUDUser = Depends(get_user_crud)
):
    hero = await user.create(data=data)
    return hero
