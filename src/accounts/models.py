from pydantic.types import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str
    email: str
    phone_number: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Mark Doe",
                "email": "mark@gmail.com",
                "phone_number": "01630811624",
            }
        }


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Mark Doe",
                "email": "mark@gmail.com",
                "phone_number": "01630811624",
            }
        }
