"""Tests cho admin module."""

import pytest
from sqlmodel import Session
from app.modules.admin.admin_models import Role, UserRoleLink
from app.modules.admin.admin_schemas import UpdateRoleRequest, InviteStaffRequest


def test_role_enum():
    """Test enum Role."""
    assert Role.CUSTOMER == "customer"
    assert Role.ADMIN == "admin"


def test_user_role_link_model():
    """Test UserRoleLink model."""
    link = UserRoleLink(user_id="123", role_name=Role.ADMIN)
    assert link.user_id == "123"
    assert link.role_name == "admin"


def test_update_role_request():
    """Test UpdateRoleRequest schema."""
    req = UpdateRoleRequest(role="technician")
    assert req.role == "technician"


def test_invite_staff_request():
    """Test InviteStaffRequest schema."""
    req = InviteStaffRequest(email="test@example.com", role="receptionist")
    assert req.email == "test@example.com"
    assert req.role == "receptionist"
