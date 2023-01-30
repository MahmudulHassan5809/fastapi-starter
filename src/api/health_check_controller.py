from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=['Health Check']
)


@router.get("/")
def read_root():
    return {"Hello": "World"}
