"""Schemas khách hàng sử dụng Pydantic."""

from datetime import date, datetime
from pydantic import BaseModel
from uuid import UUID


class ProfileBase(BaseModel):
    """Schema cơ sở cho profile."""

    email: str
    full_name: str | None = None
    phone: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None
    role: str = "customer"


class ProfileResponse(ProfileBase):
    """Schema phản hồi với thời gian."""

    id: UUID
    created_at: datetime
    updated_at: datetime


class ProfileUpdate(BaseModel):
    """Schema cập nhật cho thay đổi một phần."""

    full_name: str | None = None
    phone: str | None = None
    birth_date: date | None = None
    avatar_url: str | None = None