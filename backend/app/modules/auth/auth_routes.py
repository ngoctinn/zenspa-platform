"""
Auth Routes: API endpoints cho xác thực và quản lý roles.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import CurrentUser, get_current_user, require_admin
from app.core.database import get_session
from app.modules.auth.auth_models import Profile, UserRole
from app.modules.auth.auth_schemas import (
    ProfileResponse,
    RoleInfo,
    UserResponse,
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
