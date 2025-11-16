"""Lớp dịch vụ khách hàng."""

from sqlmodel import Session, select
from app.modules.admin.admin_models import UserRoleLink
from .customer_models import Profile


def get_profile_by_id(session: Session, user_id: str) -> Profile | None:
    """Lấy profile theo ID người dùng."""
    return session.query(Profile).filter(Profile.id == user_id).first()


def get_profile_with_roles(session: Session, user_id: str) -> dict | None:
    """Lấy profile với list roles từ UserRoleLink."""
    profile = get_profile_by_id(session, user_id)
    if not profile:
        return None

    # Get roles
    roles_result = session.exec(
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


def create_profile(session: Session, profile: Profile) -> Profile:
    """Tạo profile mới."""
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def update_profile(session: Session, profile: Profile, update_data: dict) -> Profile:
    """Cập nhật profile với dữ liệu mới."""
    for key, value in update_data.items():
        setattr(profile, key, value)
    session.commit()
    session.refresh(profile)
    return profile
