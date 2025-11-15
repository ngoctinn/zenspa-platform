"""
Auth Routes: API endpoints cho xác thực và quản lý roles.
"""

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.core.auth import CurrentUser, get_current_user, require_admin
from app.core.config import settings
from app.core.database import get_session
from app.core.security import get_client_ip, get_user_agent
from app.modules.auth.auth_models import AuditLog, Profile, UserRole
from app.modules.auth.auth_schemas import (
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
from app.modules.auth.auth_service import assign_role, create_user_profile, revoke_role
from app.modules.auth.webhook import (
    extract_user_data_from_record,
    validate_webhook_payload,
    verify_supabase_signature,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Lấy thông tin user hiện tại",
    description="Trả về thông tin user, roles và profile từ JWT token",
)
async def get_current_user_info(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UserResponse:
    """
    Endpoint GET /auth/me - Lấy thông tin user hiện tại.
    
    Yêu cầu:
    - Header: Authorization: Bearer <JWT_TOKEN>
    
    Returns:
    - UserResponse: Thông tin user, roles, profile
    """
    # Load roles từ DB (không dùng cache để có thông tin đầy đủ)
    stmt = select(UserRole).where(UserRole.user_id == current_user.user_id)
    user_roles = session.exec(stmt).all()
    
    if not user_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không có roles nào",
        )
    
    # Convert sang RoleInfo
    roles_info = [
        RoleInfo(
            role=ur.role,
            is_primary=ur.is_primary,
            assigned_at=ur.assigned_at,
            assigned_by=ur.assigned_by,
        )
        for ur in user_roles
    ]
    
    # Load profile
    profile_stmt = select(Profile).where(Profile.user_id == current_user.user_id)
    profile_obj = session.exec(profile_stmt).first()
    
    profile_response = None
    if profile_obj:
        profile_response = ProfileResponse.model_validate(profile_obj)
    
    return UserResponse(
        user_id=UUID(current_user.user_id),
        email=current_user.email,
        roles=roles_info,
        profile=profile_response,
    )


@router.post(
    "/roles",
    response_model=AssignRoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Gán role cho user (Admin only)",
    description="Admin gán role mới cho user. Idempotent - không lỗi nếu role đã tồn tại.",
)
async def assign_user_role(
    request_data: AssignRoleRequest,
    request: Request,
    current_user: CurrentUser = Depends(require_admin),
    session: Session = Depends(get_session),
) -> AssignRoleResponse:
    """
    Endpoint POST /auth/roles - Admin gán role cho user.
    
    Yêu cầu:
    - Role: admin
    - Body: AssignRoleRequest (user_id, role, is_primary, reason)
    
    Returns:
    - AssignRoleResponse: Thông báo kết quả
    """
    # Validate user tồn tại (check trong user_roles hoặc profiles)
    stmt = select(Profile).where(Profile.user_id == str(request_data.user_id))
    profile = session.exec(stmt).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {request_data.user_id} không tồn tại",
        )
    
    # Gán role
    try:
        user_role = assign_role(
            session=session,
            user_id=request_data.user_id,
            role=request_data.role,
            assigned_by=current_user.user_id,
            is_primary=request_data.is_primary,
            reason=request_data.reason,
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request),
        )
        
        return AssignRoleResponse(
            message=f"Đã gán role '{request_data.role}' cho user",
            user_id=request_data.user_id,
            role=user_role.role,
            is_primary=user_role.is_primary,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/roles/{user_id}/{role}",
    response_model=RevokeRoleResponse,
    summary="Xóa role của user (Admin only)",
    description="Admin xóa role của user. Idempotent - không lỗi nếu role không tồn tại.",
)
async def revoke_user_role(
    user_id: UUID,
    role: str,
    request: Request,
    request_data: RevokeRoleRequest | None = None,
    current_user: CurrentUser = Depends(require_admin),
    session: Session = Depends(get_session),
) -> RevokeRoleResponse:
    """
    Endpoint DELETE /auth/roles/{user_id}/{role} - Admin xóa role của user.
    
    Yêu cầu:
    - Role: admin
    - Path params: user_id, role
    - Body (optional): RevokeRoleRequest (reason)
    
    Returns:
    - RevokeRoleResponse: Thông báo kết quả
    """
    # Validate role
    valid_roles = ["customer", "receptionist", "technician", "admin"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role '{role}' không hợp lệ. Phải là: {', '.join(valid_roles)}",
        )
    
    # Xóa role
    reason = request_data.reason if request_data else None
    
    revoked = revoke_role(
        session=session,
        user_id=user_id,
        role=role,
        revoked_by=current_user.user_id,
        reason=reason,
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
    )
    
    if not revoked:
        # Idempotent: Không lỗi nếu role không tồn tại
        return RevokeRoleResponse(
            message=f"User không có role '{role}' (đã xóa trước đó)",
            user_id=user_id,
            role=role,
        )
    
    return RevokeRoleResponse(
        message=f"Đã xóa role '{role}' của user",
        user_id=user_id,
        role=role,
    )


@router.post(
    "/webhooks/user-created",
    response_model=WebhookResponse,
    summary="Webhook handler cho Supabase user.created event",
    description="Nhận webhook từ Supabase khi user mới đăng ký, tạo profile và gán role customer.",
    tags=["Webhooks"],
)
async def webhook_user_created(
    request: Request,
    session: Session = Depends(get_session),
) -> WebhookResponse:
    """
    Endpoint POST /auth/webhooks/user-created - Supabase webhook handler.
    
    Xử lý event khi user mới đăng ký:
    1. Verify webhook signature
    2. Validate payload
    3. Tạo profile cho user
    4. Gán role customer mặc định
    5. Log audit event
    
    Yêu cầu:
    - Header: X-Supabase-Signature (HMAC SHA256)
    - Body: WebhookUserCreatedPayload
    
    Returns:
    - WebhookResponse: Thông báo kết quả
    """
    # Lấy raw body để verify signature
    body = await request.body()
    signature = request.headers.get("X-Supabase-Signature")
    
    # Verify signature
    verify_supabase_signature(
        payload=body,
        signature=signature,
        secret=settings.supabase_webhook_secret,
    )
    
    # Parse JSON payload
    payload = await request.json()
    
    # Validate payload structure
    validate_webhook_payload(payload)
    
    # Chỉ xử lý INSERT events
    if payload["type"] != "INSERT":
        return WebhookResponse(
            message=f"Ignored event type '{payload['type']}'",
            user_id=None,
        )
    
    # Extract user data
    user_data = extract_user_data_from_record(payload["record"])
    user_id = user_data["user_id"]
    email = user_data["email"]
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Webhook payload thiếu user_id hoặc email",
        )
    
    # Tạo profile + gán role customer
    try:
        # Extract full_name từ user_metadata nếu có
        full_name = user_data["user_metadata"].get("full_name")
        
        create_user_profile(
            session=session,
            user_id=user_id,
            email=email,
            full_name=full_name,
        )
        
        return WebhookResponse(
            message="Đã tạo profile và gán role customer cho user mới",
            user_id=user_id,
        )
        
    except Exception as e:
        # Log error nhưng vẫn return 200 để Supabase không retry
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Lỗi khi xử lý webhook user.created: {e}", exc_info=True)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo profile: {str(e)}",
        )


@router.get(
    "/audit-logs",
    response_model=AuditLogsListResponse,
    summary="Query audit logs (Admin only)",
    description="Admin xem audit logs với filtering theo user_id, event_type, date range.",
)
async def get_audit_logs(
    user_id: UUID | None = None,
    event_type: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    limit: int = 100,
    offset: int = 0,
    current_user: CurrentUser = Depends(require_admin),
    session: Session = Depends(get_session),
) -> AuditLogsListResponse:
    """
    Endpoint GET /auth/audit-logs - Admin query audit logs.
    
    Yêu cầu:
    - Role: admin
    - Query params (optional):
      - user_id: Filter by user ID
      - event_type: Filter by event type
      - start_date: Filter logs >= start_date
      - end_date: Filter logs <= end_date
      - limit: Max number of logs (default 100, max 1000)
      - offset: Pagination offset (default 0)
    
    Returns:
    - AuditLogsListResponse: Paginated list of audit logs
    """
    from datetime import datetime as dt_module
    
    # Validate limit
    if limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit không được vượt quá 1000",
        )
    
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit phải >= 1",
        )
    
    # Build query
    stmt = select(AuditLog)
    
    # Apply filters
    if user_id:
        stmt = stmt.where(AuditLog.user_id == str(user_id))
    
    if event_type:
        stmt = stmt.where(AuditLog.event_type == event_type)
    
    if start_date:
        stmt = stmt.where(AuditLog.created_at >= start_date)
    
    if end_date:
        stmt = stmt.where(AuditLog.created_at <= end_date)
    
    # Count total matching records
    from sqlmodel import func
    count_stmt = select(func.count()).select_from(AuditLog)
    
    if user_id:
        count_stmt = count_stmt.where(AuditLog.user_id == str(user_id))
    if event_type:
        count_stmt = count_stmt.where(AuditLog.event_type == event_type)
    if start_date:
        count_stmt = count_stmt.where(AuditLog.created_at >= start_date)
    if end_date:
        count_stmt = count_stmt.where(AuditLog.created_at <= end_date)
    
    total = session.exec(count_stmt).one()
    
    # Order by created_at DESC (newest first)
    stmt = stmt.order_by(AuditLog.created_at.desc())
    
    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)
    
    # Execute query
    logs = session.exec(stmt).all()
    
    # Convert to response schema
    log_responses = [AuditLogResponse.model_validate(log) for log in logs]
    
    return AuditLogsListResponse(
        logs=log_responses,
        total=total,
        limit=limit,
        offset=offset,
    )

