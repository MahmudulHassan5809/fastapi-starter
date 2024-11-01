from collections.abc import Sequence

from src.core.permissions.enums import UserPermission


class Allow:
    def __init__(self, role: str, permissions: list[UserPermission]):
        self.role = role
        self.permissions = permissions


class ACL:
    def __init__(
        self, permissions: Sequence[tuple[Allow, str | int, list[UserPermission]]]
    ):
        self.permissions = permissions

    def is_allowed(
        self, role: str, user_id: str | int, permission: UserPermission
    ) -> bool:
        if not role:
            return False
        for allow, principal, perms in self.permissions:
            if allow.role == role and permission in perms:
                return True

            if principal == user_id and permission in perms:
                return True

        return False
