"""Routes API cho khách hàng."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.auth import get_current_user
from app.core.database import get_db
from .customer_schemas import ProfileResponse, ProfileUpdate
from .customer_service import get_profile_by_id, create_profile, update_profile
from .customer_models import Profile

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Lấy profile của người dùng hiện tại."""
    profile = get_profile_by_id(session, current_user["id"])
    if not profile:
        # Tạo lazy nếu chưa tồn tại
        profile = create_profile(
            session,
            Profile(
                id=current_user["id"],
                email=current_user["email"],
                full_name=current_user.get("full_name"),
            ),
        )
    return profile


@router.put("/me", response_model=ProfileResponse)
async def update_user_profile(
    update_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    """Cập nhật profile của người dùng hiện tại."""
    profile = get_profile_by_id(session, current_user["id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile không tìm thấy")
    return update_profile(session, profile, update_data.dict(exclude_unset=True))
