from enum import Enum


class ProfileStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    IN_ACTIVE = "IN_ACTIVE"
    RESTRICTED = "RESTRICTED"
    PENDING = "PENDING"


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
