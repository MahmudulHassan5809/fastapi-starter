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

    class Config:
        case_sensitive = True


settings = Settings()
