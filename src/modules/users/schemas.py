from datetime import date

from pydantic import BaseModel, ConfigDict

from src.core.helpers.enums import GenderEnum
from src.core.permissions.enums import UserGroup


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    phone: str
    gender: GenderEnum
    dob: date
    status: str
    email: str


class AdminUserProfile(UserProfile):
    group: UserGroup
    is_staff: bool = True
    is_superuser: bool = False
    model_config = ConfigDict(from_attributes=True)


class StaffCreate(AdminUserProfile):
    password: str
