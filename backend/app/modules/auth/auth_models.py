"""
Auth Models: SQLModel definitions for authentication and authorization.

Tables:
- profiles: User profile information
- user_roles: Multi-role mapping (1 user = many roles)
- audit_logs: Security event audit trail
"""

from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field
import uuid as uuid_module


class Profile(SQLModel, table=True):
    """User profile information.
    
    Stores basic user profile data linked to Supabase auth.users.
    One-to-one relationship with auth.users.
    """
    
    __tablename__ = "profiles"
    
    id: UUID = Field(
        default_factory=uuid_module.uuid4,
        primary_key=True,
        description="Unique profile ID"
    )
    user_id: UUID = Field(
        foreign_key="auth.users.id",
        unique=True,
        description="Foreign key to Supabase auth.users"
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
        description="User full name (optional, editable from frontend)"
    )
    avatar_url: str | None = Field(
        default=None,
        description="Avatar image URL (optional)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Profile creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last profile update timestamp"
    )
    
    class Config:
        """SQLModel config."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "full_name": "Nguyễn Văn A",
                "avatar_url": "https://example.com/avatar.jpg",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-15T14:30:00Z"
            }
        }


class UserRole(SQLModel, table=True):
    """User role assignment (many-to-many mapping).
    
    Supports multi-role assignment: 1 user can have multiple roles.
    Primary role indicates the default role for UI navigation.
    """
    
    __tablename__ = "user_roles"
    
    id: UUID = Field(
        default_factory=uuid_module.uuid4,
        primary_key=True,
        description="Unique role assignment ID"
    )
    user_id: UUID = Field(
        foreign_key="auth.users.id",
        description="Foreign key to Supabase auth.users"
    )
    role: str = Field(
        max_length=50,
        description="Role name: customer, receptionist, technician, admin"
    )
    assigned_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Role assignment timestamp"
    )
    assigned_by: UUID | None = Field(
        default=None,
        foreign_key="auth.users.id",
        description="User ID of admin who assigned this role (NULL for system-assigned)"
    )
    is_primary: bool = Field(
        default=False,
        description="Is this the primary role? (used for default dashboard)"
    )
    
    class Config:
        """SQLModel config."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "role": "receptionist",
                "assigned_at": "2024-01-01T12:00:00Z",
                "assigned_by": "f47ac10b-58cc-4372-a567-0e02b2c3d478",
                "is_primary": True
            }
        }


class AuditLog(SQLModel, table=True):
    """Security and business event audit log.
    
    Tracks important events for compliance, debugging, and monitoring.
    Supports flexible metadata via JSONB for different event types.
    """
    
    __tablename__ = "audit_logs"
    
    id: UUID = Field(
        default_factory=uuid_module.uuid4,
        primary_key=True,
        description="Unique audit log ID"
    )
    user_id: UUID | None = Field(
        default=None,
        foreign_key="auth.users.id",
        description="User ID who triggered event (NULL for system events)"
    )
    event_type: str = Field(
        max_length=100,
        description="Event type: user.login, role.assigned, appointment.checkin, payment.processed, etc."
    )
    metadata: dict | None = Field(
        default=None,
        description="Event-specific metadata (varies by event_type)"
    )
    ip_address: str | None = Field(
        default=None,
        description="Client IP address"
    )
    user_agent: str | None = Field(
        default=None,
        description="Client user agent string"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Event timestamp"
    )
    
    class Config:
        """SQLModel config."""
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "event_type": "role.assigned",
                "metadata": {
                    "assigned_role": "receptionist",
                    "assigned_by_id": "f47ac10b-58cc-4372-a567-0e02b2c3d478"
                },
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "created_at": "2024-01-01T12:00:00Z"
            }
        }
