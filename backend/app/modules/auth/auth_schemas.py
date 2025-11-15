"""
Pydantic schemas cho auth module.
Request/Response models cho API endpoints.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    """Response schema cho profile của user."""
    
    id: UUID = Field(description="ID của profile")
    user_id: UUID = Field(description="ID của user (auth.users)")
    full_name: str | None = Field(default=None, description="Họ tên đầy đủ")
    avatar_url: str | None = Field(default=None, description="URL ảnh đại diện")
    created_at: datetime = Field(description="Thời điểm tạo profile")
    updated_at: datetime = Field(description="Thời điểm cập nhật cuối")
    
    model_config = {"from_attributes": True}


class RoleInfo(BaseModel):
    """Thông tin về 1 role của user."""
    
    role: str = Field(description="Tên role (customer, receptionist, technician, admin)")
    is_primary: bool = Field(description="Có phải role chính không")
    assigned_at: datetime = Field(description="Thời điểm được gán role")
    assigned_by: UUID | None = Field(default=None, description="ID người gán role")


class UserResponse(BaseModel):
    """Response schema cho GET /auth/me - thông tin user hiện tại."""
    
    user_id: UUID = Field(description="ID của user")
    email: str = Field(description="Email của user")
    roles: list[RoleInfo] = Field(description="Danh sách roles của user")
    profile: ProfileResponse | None = Field(default=None, description="Profile của user")
    
    model_config = {"from_attributes": True}


class AssignRoleRequest(BaseModel):
    """Request schema cho POST /auth/roles - gán role cho user."""
    
    user_id: UUID = Field(description="ID của user cần gán role")
    role: str = Field(
        description="Role cần gán",
        pattern="^(customer|receptionist|technician|admin)$",
    )
    is_primary: bool = Field(
        default=False,
        description="Đặt làm role chính (chỉ 1 role được là primary)",
    )
    reason: str | None = Field(
        default=None,
        max_length=500,
        description="Lý do gán role (optional, dùng cho audit log)",
    )


class RevokeRoleRequest(BaseModel):
    """Request schema cho DELETE /auth/roles - xóa role của user."""
    
    reason: str | None = Field(
        default=None,
        max_length=500,
        description="Lý do xóa role (optional, dùng cho audit log)",
    )


class AssignRoleResponse(BaseModel):
    """Response schema sau khi gán role thành công."""
    
    message: str = Field(description="Thông báo kết quả")
    user_id: UUID = Field(description="ID của user")
    role: str = Field(description="Role đã gán")
    is_primary: bool = Field(description="Có phải role chính không")


class RevokeRoleResponse(BaseModel):
    """Response schema sau khi xóa role thành công."""
    
    message: str = Field(description="Thông báo kết quả")
    user_id: UUID = Field(description="ID của user")
    role: str = Field(description="Role đã xóa")


class WebhookUserCreatedPayload(BaseModel):
    """Payload từ Supabase webhook khi user mới đăng ký."""
    
    type: str = Field(description="Event type (INSERT, UPDATE, DELETE)")
    table: str = Field(description="Table name (users)")
    record: dict = Field(description="User record data")
    schema: str = Field(description="Schema name (auth)")
    old_record: dict | None = Field(default=None, description="Old record (for UPDATE/DELETE)")


class WebhookResponse(BaseModel):
    """Response cho webhook handler."""
    
    message: str = Field(description="Thông báo kết quả")
    user_id: UUID | None = Field(default=None, description="ID của user được tạo")
