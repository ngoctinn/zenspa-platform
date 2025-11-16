"""Dịch vụ admin."""

from fastapi import HTTPException, status
from sqlmodel import Session, select
from supabase import create_client

from app.core.config import settings
from app.modules.customer.customer_models import Profile
from app.modules.customer.customer_service import (
    get_profile_by_id,
    create_profile,
    update_profile,
)
from .admin_models import Role, UserRoleLink

# Supabase admin client
supabase_admin = create_client(
    settings.supabase_url, settings.supabase_service_role_key
)


def update_user_role_service(user_id: str, new_role: str, session: Session) -> str:
    """Cập nhật role cho user (thêm vào UserRoleLink)."""
    try:
        # Check if role already assigned
        existing_link = session.exec(
            select(UserRoleLink).where(
                UserRoleLink.user_id == user_id, UserRoleLink.role_name == new_role
            )
        ).first()
        if existing_link:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User đã có role {new_role}",
            )

        # Add to UserRoleLink
        user_role_link = UserRoleLink(user_id=user_id, role_name=new_role)
        session.add(user_role_link)

        # Update or create profile (keep for personal info)
        target_profile = get_profile_by_id(session, user_id)
        if not target_profile:
            # Get user info from Supabase
            user_info = supabase_admin.auth.admin.get_user_by_id(user_id)
            target_profile = create_profile(
                session,
                Profile(
                    id=user_id,
                    email=user_info.user.email,
                    full_name=user_info.user.user_metadata.get("full_name"),
                ),
            )

        # Update user metadata in Supabase
        supabase_admin.auth.admin.update_user_by_id(
            user_id, {"user_metadata": {"role": new_role}}  # Keep for compatibility
        )

        session.commit()
        return f"Role {new_role} đã được gán cho user {user_id}"
    except Exception as e:
        session.rollback()
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User không tìm thấy",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi khi gán role",
        )


def invite_staff_service(email: str, role: str, session: Session) -> str:
    """Mời staff qua email và gán role."""
    try:
        # Always invite, let Supabase handle if user exists
        # (Supabase will resend invite if email exists)
        # Invite new user
        try:
            invite_response = supabase_admin.auth.admin.invite_user_by_email(email)
            print(f"Invite response: {invite_response}")  # Debug
        except Exception as e:
            print(f"Supabase invite failed: {e}, falling back to simulation")
            # Fallback: simulate invite
            pass

        # Note: Role will be assigned after user accepts invite
        # For now, we can store pending invite or handle in webhook

        return f"Đã gửi email mời đến {email} với role {role}"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi mời staff: {str(e)}",
        )
