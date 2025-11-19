"""Routes API cho user - Consolidated từ admin và customer routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.database import get_db
from .user_models import Profile, UserRoleLink
from .user_schemas import (
    ProfileResponse,
    ProfileUpdate,
    UpdateRoleRequest,
    InviteStaffRequest,
)
from .user_service import (
    get_profile_by_id,
    create_profile,
    update_profile,
    get_profile_with_roles,
    update_user_role_service,
    invite_staff_service,
)

# Router cho user endpoints (profile management)
router = APIRouter()

# Router cho admin endpoints (role & staff management)
admin_router = APIRouter()


@router.get("/me")
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Lấy profile của người dùng hiện tại."""
    profile_data = get_profile_with_roles(session, current_user["id"])
    if not profile_data:
        # Tạo lazy nếu chưa tồn tại
        profile = create_profile(
            session,
            Profile(
                id=current_user["id"],
                email=current_user["email"],
                full_name=current_user.get("full_name"),
            ),
        )
        profile_data = {
            "id": profile.id,
            "email": profile.email,
            "full_name": profile.full_name,
            "phone": profile.phone,
            "birth_date": profile.birth_date,
            "avatar_url": profile.avatar_url,
            "roles": ["customer"],
            "created_at": profile.created_at,
            "updated_at": profile.updated_at,
        }
    return profile_data


@router.put("/me", response_model=ProfileResponse)
async def update_user_profile(
    update_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Cập nhật profile của người dùng hiện tại."""
    profile = get_profile_by_id(session, current_user["id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile không tìm thấy")
    return update_profile(session, profile, update_data.dict(exclude_unset=True))


# Admin endpoints (role & staff management)
@admin_router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    request: UpdateRoleRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Update role cho user (chỉ admin)."""
    # Check if current user is admin
    admin_link = session.exec(
        select(UserRoleLink).where(
            UserRoleLink.user_id == current_user["id"],
            UserRoleLink.role_name == "admin",
        )
    ).first()
    if not admin_link:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới có quyền update role",
        )

    # Validate role
    valid_roles = ["customer", "receptionist", "technician", "admin"]
    if request.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role không hợp lệ. Các role hợp lệ: {', '.join(valid_roles)}",
        )

    message = update_user_role_service(user_id, request.role, session)
    return {"message": message}


@admin_router.post("/invite-staff")
async def invite_staff(
    request: InviteStaffRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Mời staff qua email (chỉ admin)."""
    # Check if current user is admin
    admin_link = session.exec(
        select(UserRoleLink).where(
            UserRoleLink.user_id == current_user["id"],
            UserRoleLink.role_name == "admin",
        )
    ).first()
    if not admin_link:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới có quyền mời staff",
        )

    # Validate role
    valid_roles = ["customer", "receptionist", "technician", "admin"]
    if request.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role không hợp lệ. Các role hợp lệ: {', '.join(valid_roles)}",
        )

    message = invite_staff_service(request.email, request.role, session)
    return {"message": message}
