from datetime import date, datetime

from sqlalchemy import TIMESTAMP, Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.helpers.enums import ProfileStatusEnum
from src.core.models import BaseModel
from src.core.permissions import Allow, UserGroup, UserPermission


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)

    dob: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(15), default=ProfileStatusEnum.ACTIVE, nullable=False
    )
    is_staff: Mapped[bool] = mapped_column(default=False, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    last_logged_in_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    group: Mapped[UserGroup] = mapped_column(
        Enum(UserGroup), default=UserGroup.BASIC, nullable=True
    )

    def __acl__(self) -> Allow:
        permissions = {
            UserGroup.BASIC: [UserPermission.READ],
            UserGroup.STAFF: [UserPermission.READ, UserPermission.CREATE],
            UserGroup.MANAGER: [UserPermission.READ, UserPermission.EDIT],
            UserGroup.SUPER_ADMIN: list(UserPermission),
        }

        user_permissions = permissions.get(self.group, [])

        if self.group is None:
            return [
                (
                    Allow("anonymous", []),
                    self.id,
                    [],
                ),
            ]
        return Allow(self.group.value, user_permissions)
