from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.future import select
from src.db.db_session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/health-check",
    tags=['Health Check']
)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/songs")
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute("SELECT * FROM test")
    print(result)
    songs = result.scalars().all()
    print(songs)
    return [songs]