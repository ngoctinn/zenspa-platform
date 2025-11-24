"""Mô hình user sử dụng SQLModel."""

from datetime import date, datetime, timezone
from enum import Enum
from typing import List, Optional
from sqlalchemy import TIMESTAMP, Column, func
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID


class RoleEnum(str, Enum):
    """Enum dùng trong code để tham chiếu (không tạo type trong DB)."""

    CUSTOMER = "customer"
    RECEPTIONIST = "receptionist"
    TECHNICIAN = "technician"
    ADMIN = "admin"


class Role(SQLModel, table=True):
    """Bảng quản lý các vai trò (thay thế cho Enum cứng)."""

    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        unique=True, index=True, description="Tên vai trò (admin, customer...)"
    )
    description: str | None = Field(default=None, description="Mô tả vai trò")

    # Relationship
    user_links: List["UserRoleLink"] = Relationship(back_populates="role")


class Profile(SQLModel, table=True):
    """Mô hình Profile cho user."""

    __tablename__ = "profiles"

    id: UUID = Field(
        primary_key=True, description="ID người dùng từ Supabase auth.users"
    )
    # Đã xóa cột email để tránh trùng lặp với auth.users
    full_name: str | None = Field(default=None, description="Họ và tên đầy đủ")
    phone: str | None = Field(default=None, description="Số điện thoại")
    birth_date: date | None = Field(default=None, description="Ngày sinh")
    avatar_url: str | None = Field(default=None, description="URL ảnh đại diện")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        ),
        description="Thời gian tạo (UTC)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
        description="Thời gian cập nhật (UTC)",
    )


class UserRoleLink(SQLModel, table=True):
    """Bảng liên kết user và role (nhiều-nhiều)."""

    __tablename__ = "user_role_links"

    user_id: UUID = Field(
        primary_key=True, description="ID người dùng từ Supabase auth.users"
    )
    role_id: int = Field(
        primary_key=True, foreign_key="roles.id", description="ID của role"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
        ),
        description="Thời gian tạo (UTC)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
        description="Thời gian cập nhật (UTC)",
    )

    role: Role = Relationship(back_populates="user_links")
