"""Routes API cho admin."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.auth import get_current_user
from app.core.database import get_db
from app.modules.customer.customer_models import Profile
from app.modules.customer.customer_service import get_profile_by_id, create_profile
from .admin_schemas import UpdateRoleRequest
from .admin_service import update_user_role_service

router = APIRouter()


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    request: UpdateRoleRequest,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Update role cho user (chỉ admin)."""
    # Get or create profile for current user
    profile = get_profile_by_id(session, current_user["id"])
    if not profile:
        profile = create_profile(
            session,
            Profile(
                id=current_user["id"],
                email=current_user["email"],
                full_name=current_user.get("full_name"),
            ),
        )

    # Check if current user is admin
    if profile.role != "admin":
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
