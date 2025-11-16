"""Admin API để quản lý roles và users."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from supabase import create_client

from app.core.auth import get_current_user
from app.core.config import settings

router = APIRouter()

# Supabase admin client
supabase_admin = create_client(
    settings.supabase_url, settings.supabase_service_role_key
)


class UpdateRoleRequest(BaseModel):
    """Request để update role."""

    role: str  # customer, receptionist, technician, admin


@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    request: UpdateRoleRequest,
    current_user: dict = Depends(get_current_user),
):
    """Update role cho user (chỉ admin)."""
    # Check if current user is admin
    if current_user["role"] != "admin":
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

    try:
        # Update user metadata in Supabase
        response = supabase_admin.auth.admin.update_user_by_id(
            user_id, {"user_metadata": {"role": request.role}}
        )
        return {
            "message": f"Role của user {user_id} đã được update thành {request.role}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi khi update role",
        )
