"""
Auth Routes: API endpoints cho xác thực và quản lý roles.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from app.core.auth import CurrentUser, get_current_user, require_admin
from app.core.database import get_session
from app.core.security import get_client_ip, get_user_agent
from app.modules.auth.auth_models import Profile, UserRole
from app.modules.auth.auth_schemas import (
    AssignRoleRequest,
    AssignRoleResponse,
    ProfileResponse,
    RevokeRoleRequest,
    RevokeRoleResponse,
    RoleInfo,
    UserResponse,
)
from app.modules.auth.auth_service import assign_role, revoke_role

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

