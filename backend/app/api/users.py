"""User API để lấy thông tin profile."""

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter()


@router.get("/me")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Lấy thông tin profile của user hiện tại."""
    return current_user
