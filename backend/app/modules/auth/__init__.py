"""
Auth module: Xác thực, phân quyền và nhật ký audit.

Exports:
- Models: Profile, UserRole, AuditLog
- Dependencies: get_current_user, require_role, etc.
- Services: Auth service, audit logging
- Routes: Auth endpoints
"""

from .auth_models import Profile, UserRole, AuditLog

__all__ = ["Profile", "UserRole", "AuditLog"]
