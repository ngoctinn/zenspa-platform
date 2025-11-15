"""
Auth Models: SQLModel cho xác thực và phân quyền.

Bảng:
- profiles: Thông tin hồ sơ người dùng
- user_roles: Gán nhiều vai trò (1 user = nhiều roles)
- audit_logs: Nhật ký sự kiện bảo mật
"""

from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field
import uuid as uuid_module


class Profile(SQLModel, table=True):
    """Thông tin hồ sơ người dùng.

    Lưu dữ liệu cơ bản của user, liên kết với Supabase auth.users.
    Quan hệ one-to-one với auth.users.
    """

    __tablename__ = "profiles"

    id: UUID = Field(
        default_factory=uuid_module.uuid4,
        primary_key=True,
        description="ID hồ sơ duy nhất",
    )
    user_id: UUID = Field(
        foreign_key="auth.users.id",
        unique=True,
        description="Khóa ngoại tới auth.users",
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="Họ tên đầy đủ (tùy chọn, có thể sửa từ frontend)",
    )
    avatar_url: str | None = Field(
        default=None, description="URL ảnh đại diện (tùy chọn)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời điểm tạo hồ sơ"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời điểm cập nhật gần nhất"
    )

    class Config:
        """Cấu hình SQLModel."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "full_name": "Nguyễn Văn A",
                "avatar_url": "https://example.com/avatar.jpg",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-15T14:30:00Z",
            }
        }


class UserRole(SQLModel, table=True):
    """Gán vai trò cho người dùng (many-to-many).

    Hỗ trợ đa vai trò: 1 user có thể có nhiều roles.
    Primary role xác định dashboard mặc định khi đăng nhập.
    """

    __tablename__ = "user_roles"

    id: UUID = Field(
        default_factory=uuid_module.uuid4,
        primary_key=True,
        description="ID gán role duy nhất",
    )
    user_id: UUID = Field(
        foreign_key="auth.users.id", description="Khóa ngoại tới auth.users"
    )
    role: str = Field(
        max_length=50,
        description="Tên vai trò: customer, receptionist, technician, admin",
    )
    assigned_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời điểm gán role"
    )
    assigned_by: UUID | None = Field(
        default=None,
        foreign_key="auth.users.id",
        description="User ID của admin gán role (NULL nếu hệ thống tự gán)",
    )
    is_primary: bool = Field(
        default=False,
        description="Có phải role chính không? (dùng cho dashboard mặc định)",
    )

    class Config:
        """Cấu hình SQLModel."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "role": "receptionist",
                "assigned_at": "2024-01-01T12:00:00Z",
                "assigned_by": "f47ac10b-58cc-4372-a567-0e02b2c3d478",
                "is_primary": True,
            }
        }


class AuditLog(SQLModel, table=True):
    """Nhật ký sự kiện bảo mật và nghiệp vụ.

    Theo dõi các sự kiện quan trọng phục vụ compliance, debug và giám sát.
    Hỗ trợ metadata linh hoạt qua JSONB cho từng loại event.
    """

    __tablename__ = "audit_logs"

    id: UUID = Field(
        default_factory=uuid_module.uuid4,
        primary_key=True,
        description="ID audit log duy nhất",
    )
    user_id: UUID | None = Field(
        default=None,
        foreign_key="auth.users.id",
        description="User ID kích hoạt sự kiện (NULL nếu là event hệ thống)",
    )
    event_type: str = Field(
        max_length=100,
        description="Loại sự kiện: user.login, role.assigned, appointment.checkin, payment.processed, etc.",
    )
    metadata: dict | None = Field(
        default=None,
        description="Metadata theo từng loại event (linh hoạt theo event_type)",
    )
    ip_address: str | None = Field(default=None, description="Địa chỉ IP của client")
    user_agent: str | None = Field(
        default=None, description="Chuỗi user agent của client"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Thời điểm xảy ra sự kiện"
    )

    class Config:
        """Cấu hình SQLModel."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "event_type": "role.assigned",
                "metadata": {
                    "assigned_role": "receptionist",
                    "assigned_by_id": "f47ac10b-58cc-4372-a567-0e02b2c3d478",
                },
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "created_at": "2024-01-01T12:00:00Z",
            }
        }
