import enum

class UserStatusType(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    CONTENT_CREATOR = "content_creator"