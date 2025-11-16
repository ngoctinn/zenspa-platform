"""Mô hình user sử dụng SQLModel."""

from datetime import date, datetime
from enum import Enum
from sqlmodel import Field, SQLModel
from uuid import UUID


class Role(str, Enum):
    """Enum cho vai trò người dùng."""

    CUSTOMER = "customer"
    RECEPTIONIST = "receptionist"
    TECHNICIAN = "technician"
    ADMIN = "admin"


class Profile(SQLModel, table=True):
    """Mô hình Profile cho user."""

    __tablename__ = "profiles"

    id: UUID = Field(
        primary_key=True, description="ID người dùng từ Supabase auth.users"
    )
    email: str = Field(description="Email người dùng")
    full_name: str | None = Field(default=None, description="Họ và tên đầy đủ")
    phone: str | None = Field(default=None, description="Số điện thoại")
    birth_date: date | None = Field(default=None, description="Ngày sinh")
    avatar_url: str | None = Field(default=None, description="URL ảnh đại diện")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời gian tạo"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời gian cập nhật"
    )
    role: str = Field(
        default="customer",
        description="Vai trò người dùng (for Supabase compatibility)",
    )


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
