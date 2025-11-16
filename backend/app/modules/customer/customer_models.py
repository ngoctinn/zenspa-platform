"""Mô hình khách hàng sử dụng SQLModel."""

from datetime import date, datetime
from sqlmodel import Field, SQLModel
from uuid import UUID


class Profile(SQLModel, table=True):
    """Mô hình Profile cho khách hàng."""

    __tablename__ = "profiles"

    id: UUID = Field(primary_key=True, description="ID người dùng từ Supabase auth.users")
    email: str = Field(description="Email người dùng")
    full_name: str | None = Field(default=None, description="Họ và tên đầy đủ")
    phone: str | None = Field(default=None, description="Số điện thoại")
    birth_date: date | None = Field(default=None, description="Ngày sinh")
    avatar_url: str | None = Field(default=None, description="URL ảnh đại diện")
    role: str = Field(default="customer", description="Vai trò người dùng")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Thời gian tạo")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Thời gian cập nhật")