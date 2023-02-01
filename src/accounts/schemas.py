from typing import Optional
from pydantic import BaseModel



class UserLogin(BaseModel):
    email : str
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]