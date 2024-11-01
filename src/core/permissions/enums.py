from enum import Enum


class UserPermission(Enum):
    CREATE = "CREATE"
    READ = "READ"
    EDIT = "EDIT"
    DELETE = "DELETE"


class UserGroup(Enum):
    BASIC = "BASIC"
    STAFF = "STAFF"
    MANAGER = "MANAGER"
    SUPER_ADMIN = "SUPER_ADMIN"
