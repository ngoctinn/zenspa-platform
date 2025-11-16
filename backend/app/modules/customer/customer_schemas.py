"""Schemas khách hàng sử dụng Pydantic."""

from datetime import date, datetime
from pydantic import BaseModel, Field
from uuid import UUID


class ProfileBase(BaseModel):
    """Schema cơ sở cho profile."""

    email: str
    full_name: str | None = None
    phone: str | None = Field(None, pattern=r"^\+?\d{10,15}$")
    birth_date: date | None = Field(None, ge=date(1900, 1, 1))
    avatar_url: str | None = None
    roles: list[str] = ["customer"]  # List of roles from UserRoleLink


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
