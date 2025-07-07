from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.core.models import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
