from src.core.permissions.enums import UserPermission


class Allow:
    def __init__(self, role: str, permissions: list[UserPermission]):
        self.role = role
        self.permissions = permissions


class ACL:
    def __init__(self, allow: Allow):
        self.allowed_permissions = allow.permissions
        self.allowed_group = allow.role

    def is_allowed(
        self,
        role: str,
        permission: UserPermission,
    ) -> bool:
        if not role:
            return False

        if self.allowed_group == role and permission in self.allowed_permissions:
            return True

        return False
