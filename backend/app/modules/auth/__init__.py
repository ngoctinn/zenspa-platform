"""
Auth module: Xác thực, phân quyền và nhật ký audit.

Exports:
- Models: Profile, UserRole, AuditLog
- Schemas: UserResponse, ProfileResponse, AssignRoleRequest, etc.
- Router: auth_router
"""

from .auth_models import AuditLog, Profile, UserRole
from .auth_routes import router as auth_router
from .auth_schemas import (
    AssignRoleRequest,
    AssignRoleResponse,
    AuditLogResponse,
    AuditLogsListResponse,
    ProfileResponse,
    RevokeRoleRequest,
    RevokeRoleResponse,
    RoleInfo,
    UserResponse,
    WebhookResponse,
    WebhookUserCreatedPayload,
)

__all__ = [
    # Models
    "Profile",
    "UserRole",
    "AuditLog",
    # Schemas
    "UserResponse",
    "ProfileResponse",
    "RoleInfo",
    "AssignRoleRequest",
    "AssignRoleResponse",
    "RevokeRoleRequest",
    "RevokeRoleResponse",
    "WebhookUserCreatedPayload",
    "WebhookResponse",
    "AuditLogResponse",
    "AuditLogsListResponse",
    # Router
    "auth_router",
]
