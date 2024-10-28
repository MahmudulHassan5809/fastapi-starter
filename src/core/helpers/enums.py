from enum import Enum


class ProfileStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    RESTRICTED = "RESTRICTED"
    PENDING = "PENDING"


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
