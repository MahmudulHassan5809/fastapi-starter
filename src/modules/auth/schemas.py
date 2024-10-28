from datetime import date, datetime

from pydantic import BaseModel

from src.core.helpers.enums import GenderEnum


class AuthBase(BaseModel):
    email: str
    password: str


class UserRegister(AuthBase):
    name: str
    dob: date
    phone: str
    gender: GenderEnum


class AccessTokenPayload(BaseModel):
    user_id: str
    email: str
    exp: datetime | None = None
    sub: str = "access"


class RefreshTokenPayload(BaseModel):
    user_id: str
    exp: datetime | None = None
    sub: str = "refresh"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserLogin(AuthBase):
    pass
