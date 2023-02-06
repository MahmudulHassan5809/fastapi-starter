import pathlib
from pydantic import BaseSettings, EmailStr

class Settings(BaseSettings):
    API_V1_STR: str 
    DEBUG: bool
    PROJECT_NAME: str
    VERSION: str
    DESCRIPTION: str

    DATABASE_URI: str
    SUPER_USER_EMAIL: EmailStr
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True


settings = Settings()
