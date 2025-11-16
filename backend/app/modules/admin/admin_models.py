"""Mô hình admin sử dụng SQLModel."""

from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel
from uuid import UUID


class Role(str, Enum):
    """Enum cho vai trò người dùng."""

    CUSTOMER = "customer"
    RECEPTIONIST = "receptionist"
    TECHNICIAN = "technician"
    ADMIN = "admin"


class UserRoleLink(SQLModel, table=True):
    """Bảng liên kết user và role (nhiều-nhiều)."""

    __tablename__ = "user_role_links"

    user_id: UUID = Field(
        primary_key=True, description="ID người dùng từ Supabase auth.users"
    )
    role_name: Role = Field(primary_key=True, description="Tên vai trò")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời gian tạo"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời gian cập nhật"
    )
