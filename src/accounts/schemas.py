from typing import Optional
from pydantic import BaseModel



class Token(BaseModel):
    access_token : str
    refresh_token : str

class TokenData(BaseModel):
    id : Optional[str]


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }
