from datetime import datetime, timezone
from typing import Literal
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, DateTime, Enum, String

from app.core.db import Base
from app.core.constants import RoleEnum


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="role_enum", native_enum=False,), default=RoleEnum.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(tz=timezone.utc))
