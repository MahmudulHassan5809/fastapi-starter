from fastapi import APIRouter
from src.accounts.schemas import TokenData, UserLogin

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=TokenData)
async def login(data: UserLogin):
    pass

