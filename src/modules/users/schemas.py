from datetime import date

from pydantic import BaseModel

from src.core.helpers.enums import GenderEnum
from src.core.permissions.enums import UserGroup


class UserProfile(BaseModel):
    name: str
    phone: str
    gender: GenderEnum
    dob: date
    status: str
    email: str


class AdminUserProfile(UserProfile):
    group: UserGroup
    is_staff: bool
    is_superuser: bool
