"""Schemas cho admin API."""

from pydantic import BaseModel


class UpdateRoleRequest(BaseModel):
    """Request để update role."""

    role: str  # customer, receptionist, technician, admin
