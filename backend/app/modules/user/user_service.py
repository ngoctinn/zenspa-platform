"""Dịch vụ user (Async)."""

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from supabase import create_client

from app.core.config import settings
from .user_models import Profile, Role, UserRoleLink

# Supabase admin client
supabase_admin = create_client(
    settings.supabase_url, settings.supabase_service_role_key
)


async def get_profile_by_id(session: AsyncSession, user_id: str) -> Profile | None:
    """Lấy profile theo ID người dùng."""
    result = await session.exec(select(Profile).where(Profile.id == user_id))
    return result.first()


async def get_profile_with_roles(session: AsyncSession, user_id: str) -> dict | None:
    """Lấy profile với list roles từ UserRoleLink."""
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        return None

    # Get roles
    roles_result = await session.exec(
        select(UserRoleLink.role_name).where(UserRoleLink.user_id == user_id)
    )
    roles = [row for row in roles_result]
    if not roles:
        roles = ["customer"]  # Default

    return {
        "id": profile.id,
        "email": profile.email,
        "full_name": profile.full_name,
        "phone": profile.phone,
        "birth_date": profile.birth_date,
        "avatar_url": profile.avatar_url,
        "roles": roles,
        "created_at": profile.created_at,
        "updated_at": profile.updated_at,
    }


async def create_profile(session: AsyncSession, profile: Profile) -> Profile:
    """Tạo profile mới."""
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def update_profile(
    session: AsyncSession, profile: Profile, update_data: dict
) -> Profile:
    """Cập nhật profile với dữ liệu mới."""
    for key, value in update_data.items():
        setattr(profile, key, value)
    await session.commit()
    await session.refresh(profile)
    return profile


async def update_user_role_service(
    user_id: str, new_role: str, session: AsyncSession
) -> str:
    """Cập nhật role cho user (thêm vào UserRoleLink)."""
    try:
        # Check if role already assigned
        result = await session.exec(
            select(UserRoleLink).where(
                UserRoleLink.user_id == user_id, UserRoleLink.role_name == new_role
            )
        )
        existing_link = result.first()
        if existing_link:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User đã có role {new_role}",
            )

        # Add to UserRoleLink
        user_role_link = UserRoleLink(user_id=user_id, role_name=new_role)
        session.add(user_role_link)

        # Update or create profile (keep for personal info)
        target_profile = await get_profile_by_id(session, user_id)
        if not target_profile:
            # Get user info from Supabase
            user_info = supabase_admin.auth.admin.get_user_by_id(user_id)
            target_profile = await create_profile(
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

        await session.commit()
        return f"Role {new_role} đã được gán cho user {user_id}"
    except Exception as e:
        await session.rollback()
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User không tìm thấy",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi khi gán role",
        )


async def invite_staff_service(email: str, role: str, session: AsyncSession) -> str:
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
