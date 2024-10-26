from datetime import date
from pydantic import BaseModel

from src.core.helpers.enums import GenderEnum


class AuthBase(BaseModel):
    phone: str
    password: str


class UserRegister(AuthBase):
    name: str
    dob: date
    gender: GenderEnum


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
