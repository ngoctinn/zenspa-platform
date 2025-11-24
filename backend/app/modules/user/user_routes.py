"""Routes API cho user - Consolidated từ admin và customer routes."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_async_session
from .user_models import Profile, Role, RoleEnum, UserRoleLink
from .user_schemas import (
    ProfileResponse,
    ProfileUpdate,
    UpdateRoleRequest,
    InviteStaffRequest,
)
from .user_service import (
    get_profile_by_id,
    create_profile,
    update_profile,
    get_profile_with_roles,
    update_user_role_service,
    invite_staff_service,
)

router = APIRouter()
admin_router = APIRouter()


# Dependency để check quyền admin
async def require_admin(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Dependency yêu cầu user phải có role admin."""
    user_id = current_user["id"]

    # Join với bảng Role để check tên role
    statement = (
        select(UserRoleLink)
        .join(Role)
        .where(UserRoleLink.user_id == user_id, Role.name == RoleEnum.ADMIN.value)
    )
    result = await session.exec(statement)

    if not result.first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yêu cầu quyền admin",
        )
    return current_user


@router.get("/me", response_model=ProfileResponse)
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> ProfileResponse:
    """Lấy profile của người dùng hiện tại."""
    user_id = current_user["id"]
    email = current_user.get("email")  # Lấy email từ JWT

    profile_data = await get_profile_with_roles(session, user_id, email)

    if not profile_data:
        # Tạo lazy nếu chưa tồn tại
        profile = await create_profile(
            session,
            {
                "id": user_id,
                "email": email,  # Truyền email để service xử lý (nhưng không lưu vào DB)
                "full_name": current_user.get("user_metadata", {}).get("full_name"),
            },
        )
        # Lấy lại thông tin đầy đủ sau khi tạo
        profile_data = await get_profile_with_roles(session, user_id, email)

    return ProfileResponse(**profile_data)


@router.put("/me", response_model=ProfileResponse)
async def update_user_profile(
    update_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> ProfileResponse:
    """Cập nhật profile của người dùng hiện tại."""
    user_id = current_user["id"]
    email = current_user.get("email")

    profile = await get_profile_by_id(session, user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile không tìm thấy"
        )

    updated_profile = await update_profile(
        session, profile, update_data.model_dump(exclude_unset=True)
    )
    profile_data = await get_profile_with_roles(session, updated_profile.id, email)
    return ProfileResponse(**profile_data)


# Admin endpoints
@admin_router.put(
    "/users/{user_id}/role",
    dependencies=[Depends(require_admin)],
    tags=["Admin"],
)
async def update_user_role(
    user_id: UUID,
    request: UpdateRoleRequest,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Cập nhật role cho user (chỉ admin).
    - **customer**: Khách hàng
    - **receptionist**: Lễ tân
    - **technician**: Kỹ thuật viên
    - **admin**: Quản trị viên
    """

    message = await update_user_role_service(user_id, request.role, session)
    return {"message": message}


@admin_router.post(
    "/invite-staff",
    dependencies=[Depends(require_admin)],
    tags=["Admin"],
)
async def invite_staff(
    request: InviteStaffRequest,
    session: AsyncSession = Depends(get_async_session),
):
    """Mời nhân viên mới qua email và gán vai trò (chỉ admin)."""
    message = await invite_staff_service(request.email, request.role, session)
    return {"message": message}
