"""Dịch vụ admin."""

from fastapi import HTTPException, status
from sqlmodel import Session
from supabase import create_client

from app.core.config import settings
from app.modules.customer.customer_models import Profile
from app.modules.customer.customer_service import (
    get_profile_by_id,
    create_profile,
    update_profile,
)

# Supabase admin client
supabase_admin = create_client(
    settings.supabase_url, settings.supabase_service_role_key
)


def update_user_role_service(user_id: str, new_role: str, session: Session) -> str:
    """Cập nhật role cho user."""
    try:
        # Get or create profile for target user
        target_profile = get_profile_by_id(session, user_id)
        if not target_profile:
            # Get user info from Supabase to create profile
            user_info = supabase_admin.auth.admin.get_user_by_id(user_id)
            target_profile = create_profile(
                session,
                Profile(
                    id=user_id,
                    email=user_info.user.email,
                    full_name=user_info.user.user_metadata.get("full_name"),
                    role=new_role,  # Set new role immediately
                ),
            )
        else:
            # Update existing profile
            update_profile(session, target_profile, {"role": new_role})

        # Update user metadata in Supabase
        supabase_admin.auth.admin.update_user_by_id(
            user_id, {"user_metadata": {"role": new_role}}
        )

        return f"Role của user {user_id} đã được update thành {new_role}"
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User không tìm thấy",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi khi update role",
        )
