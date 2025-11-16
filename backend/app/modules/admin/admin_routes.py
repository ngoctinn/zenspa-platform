"""Routes API cho admin."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_user
from app.core.database import get_db
from app.modules.admin.admin_models import UserRoleLink
from app.modules.customer.customer_service import get_profile_by_id, create_profile
from .admin_schemas import UpdateRoleRequest, InviteStaffRequest
from .admin_service import update_user_role_service, invite_staff_service

router = APIRouter()


@router.put("/users/{user_id}/role")
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


@router.post("/invite-staff")
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
