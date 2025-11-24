"""Schemas user sử dụng Pydantic."""

from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from .user_models import RoleEnum


class ProfileBase(BaseModel):
    """Schema cơ sở cho profile."""

    # Email không lưu trong DB profile nữa, nhưng vẫn dùng trong schema để trả về client
    email: str | None = None
    full_name: str | None = None
    phone: str | None = Field(None, pattern=r"^\+?\d{10,15}$")
    birth_date: date | None = Field(None, ge=date(1900, 1, 1))
    avatar_url: str | None = None
    roles: list[str] = ["customer"]  # List of role names


class ProfileResponse(ProfileBase):
    """Schema phản hồi với thời gian."""

    id: UUID
    created_at: datetime
    updated_at: datetime


class ProfileUpdate(BaseModel):
    """Schema cập nhật cho thay đổi một phần."""

    full_name: str | None = None
    phone: str | None = Field(None, pattern=r"^\+?\d{10,15}$")
    birth_date: date | None = Field(None, ge=date(1900, 1, 1))
    avatar_url: str | None = None


class UpdateRoleRequest(BaseModel):
    """Request để update role."""

    role: RoleEnum  # customer, receptionist, technician, admin


class InviteStaffRequest(BaseModel):
    """Request để mời staff."""

    email: EmailStr
    role: RoleEnum  # customer, receptionist, technician, admin
