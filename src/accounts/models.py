import enum
from pydantic.types import Optional
from sqlmodel import Field, SQLModel, Enum, Column
from src.core.helpers.type_choices import UserStatusType


class UserBase(SQLModel):
    name: str
    email: str
    username: str = Field(unique=True)
    phone_number: Optional[str] = None
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    type: UserStatusType = Field(sa_column=Column(Enum(UserStatusType)))

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
    password: str


class UserCreate(UserBase):
    password: str


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
