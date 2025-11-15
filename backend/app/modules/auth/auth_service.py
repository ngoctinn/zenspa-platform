"""
Auth Service: Business logic cho xác thực và quản lý roles.
Xử lý assign/revoke roles, audit logging, cache invalidation.
"""

import logging
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlmodel import Session, select

from app.modules.auth.auth_models import AuditLog, UserRole
from app.redis.client import get_redis_client

logger = logging.getLogger(__name__)


def invalidate_user_cache(user_id: str | UUID) -> None:
    """
    Xóa cache của user trong Redis.
    Gọi khi roles thay đổi để force reload từ DB.
    
    Args:
        user_id: UUID của user cần xóa cache
    """
    redis_client = get_redis_client()
    cache_key = f"user:{user_id}:roles"
    
    deleted = redis_client.delete(cache_key)
    if deleted:
        logger.info(f"Đã xóa cache cho user {user_id}")
    else:
        logger.debug(f"Không có cache cho user {user_id}")


def log_audit_event(
    session: Session,
    user_id: str | UUID | None,
    event_type: str,
    metadata: dict[str, Any] | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> AuditLog:
    """
    Ghi log audit event vào database.
    
    Args:
        session: SQLModel session
        user_id: UUID của user thực hiện action (None nếu là system)
        event_type: Loại event (role.assigned, role.revoked, user.login, etc.)
        metadata: JSONB metadata theo event type
        ip_address: IP address của client
        user_agent: User agent string
        
    Returns:
        AuditLog object đã tạo
    """
    # Convert UUID to string nếu cần
    user_id_str = str(user_id) if user_id else None
    
    audit_log = AuditLog(
        user_id=user_id_str,
        event_type=event_type,
        metadata=metadata or {},
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    session.add(audit_log)
    session.commit()
    session.refresh(audit_log)
    
    logger.info(f"Audit log created: {event_type} for user {user_id}")
    return audit_log


def assign_role(
    session: Session,
    user_id: str | UUID,
    role: str,
    assigned_by: str | UUID,
    is_primary: bool = False,
    reason: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> UserRole:
    """
    Gán role cho user (idempotent - không lỗi nếu đã tồn tại).
    
    Args:
        session: SQLModel session
        user_id: UUID của user cần gán role
        role: Role cần gán (customer, receptionist, technician, admin)
        assigned_by: UUID của user thực hiện việc gán
        is_primary: Đặt làm role chính (sẽ unset role khác)
        reason: Lý do gán role (optional, cho audit log)
        ip_address: IP address của client
        user_agent: User agent string
        
    Returns:
        UserRole object (existing hoặc newly created)
        
    Raises:
        ValueError: Nếu role không hợp lệ
    """
    # Validate role
    valid_roles = ["customer", "receptionist", "technician", "admin"]
    if role not in valid_roles:
        raise ValueError(f"Role '{role}' không hợp lệ. Phải là: {', '.join(valid_roles)}")
    
    # Convert UUID to string
    user_id_str = str(user_id)
    assigned_by_str = str(assigned_by)
    
    # Check xem role đã tồn tại chưa
    stmt = select(UserRole).where(
        UserRole.user_id == user_id_str,
        UserRole.role == role,
    )
    existing_role = session.exec(stmt).first()
    
    if existing_role:
        logger.info(f"User {user_id} đã có role '{role}', skip assign")
        
        # Update is_primary nếu cần
        if is_primary and not existing_role.is_primary:
            # Unset primary cho các roles khác
            _unset_primary_roles(session, user_id_str, exclude_role=role)
            existing_role.is_primary = True
            session.add(existing_role)
            session.commit()
            session.refresh(existing_role)
            logger.info(f"Đã update role '{role}' thành primary cho user {user_id}")
        
        return existing_role
    
    # Nếu is_primary = True, unset các role khác
    if is_primary:
        _unset_primary_roles(session, user_id_str)
    
    # Tạo role mới
    user_role = UserRole(
        user_id=user_id_str,
        role=role,
        assigned_by=assigned_by_str,
        is_primary=is_primary,
    )
    
    session.add(user_role)
    session.commit()
    session.refresh(user_role)
    
    logger.info(f"Đã gán role '{role}' cho user {user_id}")
    
    # Log audit event
    metadata = {
        "assigned_role": role,
        "assigned_by_id": assigned_by_str,
        "is_primary": is_primary,
    }
    if reason:
        metadata["reason"] = reason
    
    log_audit_event(
        session=session,
        user_id=user_id_str,
        event_type="role.assigned",
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Invalidate cache
    invalidate_user_cache(user_id_str)
    
    return user_role


def revoke_role(
    session: Session,
    user_id: str | UUID,
    role: str,
    revoked_by: str | UUID,
    reason: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> bool:
    """
    Xóa role của user.
    
    Args:
        session: SQLModel session
        user_id: UUID của user cần xóa role
        role: Role cần xóa
        revoked_by: UUID của user thực hiện việc xóa
        reason: Lý do xóa role (optional)
        ip_address: IP address
        user_agent: User agent
        
    Returns:
        True nếu đã xóa, False nếu role không tồn tại
    """
    user_id_str = str(user_id)
    revoked_by_str = str(revoked_by)
    
    # Tìm role
    stmt = select(UserRole).where(
        UserRole.user_id == user_id_str,
        UserRole.role == role,
    )
    user_role = session.exec(stmt).first()
    
    if not user_role:
        logger.warning(f"User {user_id} không có role '{role}', skip revoke")
        return False
    
    # Xóa role
    session.delete(user_role)
    session.commit()
    
    logger.info(f"Đã xóa role '{role}' của user {user_id}")
    
    # Log audit event
    metadata = {
        "revoked_role": role,
        "revoked_by_id": revoked_by_str,
    }
    if reason:
        metadata["reason"] = reason
    
    log_audit_event(
        session=session,
        user_id=user_id_str,
        event_type="role.revoked",
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    
    # Invalidate cache
    invalidate_user_cache(user_id_str)
    
    return True


def _unset_primary_roles(
    session: Session,
    user_id: str,
    exclude_role: str | None = None,
) -> None:
    """
    Internal helper: Unset is_primary cho tất cả roles của user.
    
    Args:
        session: SQLModel session
        user_id: UUID của user
        exclude_role: Role cần exclude (không unset)
    """
    stmt = select(UserRole).where(
        UserRole.user_id == user_id,
        UserRole.is_primary == True,
    )
    
    if exclude_role:
        stmt = stmt.where(UserRole.role != exclude_role)
    
    primary_roles = session.exec(stmt).all()
    
    for role in primary_roles:
        role.is_primary = False
        session.add(role)
    
    if primary_roles:
        session.commit()
        logger.debug(f"Đã unset {len(primary_roles)} primary roles cho user {user_id}")


def get_user_roles(session: Session, user_id: str | UUID) -> list[UserRole]:
    """
    Lấy tất cả roles của user từ DB.
    
    Args:
        session: SQLModel session
        user_id: UUID của user
        
    Returns:
        List các UserRole objects
    """
    user_id_str = str(user_id)
    stmt = select(UserRole).where(UserRole.user_id == user_id_str)
    return list(session.exec(stmt).all())


def create_user_profile(
    session: Session,
    user_id: str | UUID,
    email: str,
    full_name: str | None = None,
) -> None:
    """
    Tạo profile cho user mới (gọi từ webhook handler).
    
    Args:
        session: SQLModel session
        user_id: UUID của user
        email: Email của user
        full_name: Họ tên (optional)
    """
    from app.modules.auth.auth_models import Profile
    
    user_id_str = str(user_id)
    
    # Check xem profile đã tồn tại chưa
    stmt = select(Profile).where(Profile.user_id == user_id_str)
    existing = session.exec(stmt).first()
    
    if existing:
        logger.info(f"Profile cho user {user_id} đã tồn tại, skip create")
        return
    
    # Tạo profile mới
    profile = Profile(
        user_id=user_id_str,
        full_name=full_name or email.split("@")[0],  # Default: username từ email
    )
    
    session.add(profile)
    
    # Gán role customer mặc định
    customer_role = UserRole(
        user_id=user_id_str,
        role="customer",
        is_primary=True,
        assigned_by=user_id_str,  # Self-assigned
    )
    
    session.add(customer_role)
    session.commit()
    
    logger.info(f"Đã tạo profile và gán role customer cho user {user_id}")
    
    # Log audit
    log_audit_event(
        session=session,
        user_id=user_id_str,
        event_type="user.registered",
        metadata={
            "email": email,
            "default_role": "customer",
        },
    )
