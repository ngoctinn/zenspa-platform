"""Lớp dịch vụ khách hàng."""

from sqlmodel import Session, select
from .customer_models import Profile


def get_profile_by_id(session: Session, user_id: str) -> Profile | None:
    """Lấy profile theo ID người dùng."""
    return session.query(Profile).filter(Profile.id == user_id).first()


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
