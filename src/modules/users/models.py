from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, Date, String
from src.core.helpers.enums import ProfileStatusEnum
from src.core.models import BaseModel


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
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    last_logged_in_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
