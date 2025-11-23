"""Dịch vụ user (Async)."""

from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from supabase.client import Client, create_client

from app.core.config import settings
from .user_models import Profile, Role, UserRoleLink

# Supabase admin client
supabase_admin: Client = create_client(
    settings.supabase_url, settings.supabase_service_role_key
)


async def get_profile_by_id(session: AsyncSession, user_id: UUID) -> Profile | None:
    """Lấy profile theo ID người dùng."""
    result = await session.exec(select(Profile).where(Profile.id == user_id))
    return result.first()


async def get_profile_with_roles(session: AsyncSession, user_id: UUID) -> dict | None:
    """Lấy profile với list roles từ UserRoleLink."""
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        return None

    # Get roles
    roles_result = await session.exec(
        select(UserRoleLink.role_name).where(UserRoleLink.user_id == user_id)
    )
    roles = roles_result.all()
    if not roles:
        roles.append(Role.CUSTOMER)  # Default

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


async def create_profile(session: AsyncSession, profile_data: dict) -> Profile:
    """Tạo profile mới và gán role mặc định."""
    # Tạo profile
    profile = Profile(**profile_data)
    session.add(profile)

    # Gán role mặc định là customer
    link = UserRoleLink(user_id=profile.id, role_name=Role.CUSTOMER)
    session.add(link)

    await session.commit()
    await session.refresh(profile)
    return profile


async def update_profile(
    session: AsyncSession, profile: Profile, update_data: dict
) -> Profile:
    """Cập nhật profile với dữ liệu mới."""
    for key, value in update_data.items():
        setattr(profile, key, value)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def update_user_role_service(
    user_id: UUID, new_role: Role, session: AsyncSession
) -> str:
    """Cập nhật role cho user (thêm vào UserRoleLink)."""
    # Lấy thông tin user từ DB hoặc Supabase
    target_profile = await get_profile_by_id(session, user_id)
    if not target_profile:
        try:
            user_info = supabase_admin.auth.admin.get_user_by_id(str(user_id))
            target_profile = await create_profile(
                session,
                {
                    "id": user_id,
                    "email": user_info.user.email,
                    "full_name": user_info.user.user_metadata.get("full_name"),
                },
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User với ID {user_id} không tồn tại",
            )

    # Check if role đã tồn tại
    existing_link_result = await session.exec(
        select(UserRoleLink).where(
            UserRoleLink.user_id == user_id, UserRoleLink.role_name == new_role
        )
    )
    if existing_link_result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User đã có role '{new_role.value}'",
        )

    # Add role mới
    new_link = UserRoleLink(user_id=user_id, role_name=new_role)
    session.add(new_link)
    await session.commit()

    return f"Đã gán role '{new_role.value}' cho user {user_id}"


async def invite_staff_service(email: str, role: Role, session: AsyncSession) -> str:
    """Mời staff qua email và gán role."""
    try:
        # Supabase tự động xử lý việc gửi lại invite nếu user đã tồn tại.
        supabase_admin.auth.admin.invite_user_by_email(email, data={"role": role.value})
        return f"Đã gửi email mời đến {email} với role '{role.value}'"
    except Exception as e:
        # Ghi log lỗi để debug
        print(f"Lỗi khi mời staff: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể gửi lời mời. Lỗi: {e}",
        )
