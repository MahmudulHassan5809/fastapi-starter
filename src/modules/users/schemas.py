from datetime import date

from pydantic import BaseModel

from src.core.helpers.enums import GenderEnum


class UserProfile(BaseModel):
    name: str
    phone: str
    gender: GenderEnum
    dob: date
    status: str
    email: str
