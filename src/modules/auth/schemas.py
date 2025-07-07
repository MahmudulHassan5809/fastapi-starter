from datetime import datetime

from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class AccessTokenPayload(BaseModel):
    user_id: str
    phone: str
    exp: datetime | None = None
    sub: str = "access"


class RefreshTokenPayload(BaseModel):
    user_id: str
    exp: datetime | None = None
    sub: str = "refresh"


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    profile_status: str
