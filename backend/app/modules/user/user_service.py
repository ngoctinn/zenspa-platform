"""Dịch vụ user (Async)."""

from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from supabase.client import Client, create_client

from app.core.config import settings
from app.core.logging import logger
from app.redis.helpers import cache_delete, cache_get, cache_set
from .user_models import Profile, Role, RoleEnum, UserRoleLink

# Thời gian sống cho cache hồ sơ người dùng (1 giờ)
USER_CACHE_TTL = 3600

# Supabase admin client
supabase_admin: Client = create_client(
    settings.supabase_url, settings.supabase_service_role_key
)


def _generate_user_cache_key(user_id: UUID) -> str:
    """Tạo khóa cache chuẩn cho hồ sơ người dùng."""
    return f"user_profile:{user_id}"


async def get_role_by_name(session: AsyncSession, role_name: str) -> Role:
    """Lấy role object từ DB theo tên."""
    result = await session.exec(select(Role).where(Role.name == role_name))
    role = result.first()
    if not role:
        # Nếu chưa có role trong DB (lần đầu chạy), tạo mới
        # Đây là cơ chế seed data đơn giản
        role = Role(name=role_name, description=f"Role {role_name}")
        session.add(role)
        await session.commit()
        await session.refresh(role)
    return role


async def get_profile_by_id(session: AsyncSession, user_id: UUID) -> Profile | None:
    """Lấy profile theo ID người dùng."""
    result = await session.exec(select(Profile).where(Profile.id == user_id))
    return result.first()


async def get_profile_with_roles(
    session: AsyncSession, user_id: UUID, email: str | None = None
) -> dict | None:
    """
    Lấy profile với list roles, ưu tiên từ cache.
    Áp dụng Cache-Aside Pattern.
    """
    cache_key = _generate_user_cache_key(user_id)

    # 1. Thử đọc từ cache
    cached_profile = cache_get(cache_key)
    if cached_profile:
        logger.debug(f"Cache hit cho hồ sơ người dùng: {cache_key}")
        # Nếu email được truyền vào và khác cache, update cache (optional)
        if email and cached_profile.get("email") != email:
            cached_profile["email"] = email
        return cached_profile

    logger.debug(f"Cache miss: {cache_key}. Truy vấn database...")

    # 2. Không có trong cache, truy vấn database
    profile = await get_profile_by_id(session, user_id)
    if not profile:
        return None

    # Lấy roles qua bảng liên kết và bảng roles
    # Join UserRoleLink với Role để lấy tên role
    statement = (
        select(Role.name)
        .join(UserRoleLink, UserRoleLink.role_id == Role.id)
        .where(UserRoleLink.user_id == user_id)
    )
    roles_result = await session.exec(statement)
    roles = roles_result.all()

    if not roles:
        roles = [RoleEnum.CUSTOMER.value]

    profile_data = {
        "id": profile.id,
        "email": email,  # Email lấy từ tham số (JWT/Auth), không phải từ DB profile
        "full_name": profile.full_name,
        "phone": profile.phone,
        "birth_date": profile.birth_date.isoformat() if profile.birth_date else None,
        "avatar_url": profile.avatar_url,
        "roles": roles,
        "created_at": profile.created_at.isoformat(),
        "updated_at": profile.updated_at.isoformat(),
    }

    # 3. Lưu vào cache trước khi trả về
    cache_set(cache_key, profile_data, ttl=USER_CACHE_TTL)
    logger.info(f"Đã lưu hồ sơ người dùng {user_id} vào cache.")

    return profile_data


async def create_profile(session: AsyncSession, profile_data: dict) -> Profile:
    """Tạo profile mới và gán role mặc định."""
    # Tách email ra khỏi profile_data nếu có (vì model không còn cột email)
    email = profile_data.pop("email", None)

    # Tạo profile
    profile = Profile(**profile_data)
    session.add(profile)

    # Lấy role customer từ DB
    role_customer = await get_role_by_name(session, RoleEnum.CUSTOMER.value)

    # Gán role mặc định là customer
    link = UserRoleLink(user_id=profile.id, role_id=role_customer.id)
    session.add(link)

    await session.commit()
    await session.refresh(profile)
    return profile


async def update_profile(
    session: AsyncSession, profile: Profile, update_data: dict
) -> Profile:
    """Cập nhật profile và vô hiệu hóa cache."""
    for key, value in update_data.items():
        setattr(profile, key, value)

    # Không cần set updated_at thủ công, DB sẽ tự động cập nhật

    session.add(profile)
    await session.commit()
    await session.refresh(profile)

    # Vô hiệu hóa cache sau khi cập nhật DB
    cache_key = _generate_user_cache_key(profile.id)
    if cache_delete(cache_key):
        logger.info(f"Đã vô hiệu hóa cache cho hồ sơ: {cache_key}")

    return profile


async def update_user_role_service(
    user_id: UUID, new_role_enum: RoleEnum, session: AsyncSession
) -> str:
    """Cập nhật role cho user và vô hiệu hóa cache."""
    # Lấy thông tin user từ DB hoặc Supabase
    target_profile = await get_profile_by_id(session, user_id)
    if not target_profile:
        try:
            user_info = supabase_admin.auth.admin.get_user_by_id(str(user_id))
            # Tạo profile nếu chưa có (lazy creation)
            target_profile = await create_profile(
                session,
                {
                    "id": user_id,
                    # "email": user_info.user.email, # Không lưu email
                    "full_name": user_info.user.user_metadata.get("full_name"),
                },
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User với ID {user_id} không tồn tại",
            )

    # Lấy role ID từ bảng roles
    role_obj = await get_role_by_name(session, new_role_enum.value)

    # Check if role đã tồn tại
    existing_link_result = await session.exec(
        select(UserRoleLink).where(
            UserRoleLink.user_id == user_id, UserRoleLink.role_id == role_obj.id
        )
    )
    if existing_link_result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User đã có role '{new_role_enum.value}'",
        )

    # Add role mới
    new_link = UserRoleLink(user_id=user_id, role_id=role_obj.id)
    session.add(new_link)
    await session.commit()

    # Vô hiệu hóa cache sau khi cập nhật role
    cache_key = _generate_user_cache_key(user_id)
    if cache_delete(cache_key):
        logger.info(f"Đã vô hiệu hóa cache cho hồ sơ do thay đổi role: {cache_key}")

    return f"Đã gán role '{new_role_enum.value}' cho user {user_id}"


async def invite_staff_service(
    email: str, role: RoleEnum, session: AsyncSession
) -> str:
    """Mời staff qua email và gán role."""
    try:
        # Supabase tự động xử lý việc gửi lại invite nếu user đã tồn tại.
        # Lưu ý: Supabase invite chỉ tạo user trong auth.users.
        # Việc gán role trong DB của mình sẽ cần thực hiện khi user accept invite và login lần đầu (hook)
        # Hoặc ta có thể pre-create profile và role link nếu biết UUID (nhưng invite chưa có UUID cố định cho đến khi tạo)
        # Tuy nhiên, Supabase `invite_user_by_email` trả về User object ngay lập tức.

        response = supabase_admin.auth.admin.invite_user_by_email(
            email, data={"role": role.value}
        )
        user = response.user

        if user:
            user_id = UUID(user.id)
            # Pre-create profile và role
            # Kiểm tra xem profile đã tồn tại chưa
            profile = await get_profile_by_id(session, user_id)
            if not profile:
                profile = Profile(
                    id=user_id, full_name=email.split("@")[0]
                )  # Tạm lấy tên từ email
                session.add(profile)
                await session.commit()

            # Gán role
            role_obj = await get_role_by_name(session, role.value)

            # Check exist link
            existing_link = await session.exec(
                select(UserRoleLink).where(
                    UserRoleLink.user_id == user_id, UserRoleLink.role_id == role_obj.id
                )
            )
            if not existing_link.first():
                link = UserRoleLink(user_id=user_id, role_id=role_obj.id)
                session.add(link)
                await session.commit()

        return f"Đã gửi email mời đến {email} với role '{role.value}'"
    except Exception as e:
        # Ghi log lỗi để debug
        print(f"Lỗi khi mời staff: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể gửi lời mời. Lỗi: {e}",
        )
