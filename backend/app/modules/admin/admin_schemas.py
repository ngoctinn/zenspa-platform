"""Schemas cho admin API."""

from pydantic import BaseModel, EmailStr


class UpdateRoleRequest(BaseModel):
    """Request để update role."""

    role: str  # customer, receptionist, technician, admin


class InviteStaffRequest(BaseModel):
    """Request để mời staff."""

    email: EmailStr
    role: str  # customer, receptionist, technician, admin
