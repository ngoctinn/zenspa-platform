"""Tests cho user module."""

import pytest
from sqlmodel import Session
from app.modules.user.user_models import Role, UserRoleLink, Profile
from app.modules.user.user_schemas import (
    UpdateRoleRequest,
    InviteStaffRequest,
    ProfileUpdate,
)


def test_role_enum():
    """Test enum Role."""
    assert Role.CUSTOMER == "customer"
    assert Role.ADMIN == "admin"
    assert Role.RECEPTIONIST == "receptionist"
    assert Role.TECHNICIAN == "technician"


def test_user_role_link_model():
    """Test UserRoleLink model."""
    link = UserRoleLink(user_id="123", role_name=Role.ADMIN)
    assert link.user_id == "123"
    assert link.role_name == "admin"


def test_profile_model():
    """Test Profile model."""
    profile = Profile(
        id="123",
        email="test@example.com",
        full_name="Test User",
        role="customer",
    )
    assert profile.id == "123"
    assert profile.email == "test@example.com"
    assert profile.full_name == "Test User"


def test_update_role_request():
    """Test UpdateRoleRequest schema."""
    req = UpdateRoleRequest(role="technician")
    assert req.role == "technician"


def test_invite_staff_request():
    """Test InviteStaffRequest schema."""
    req = InviteStaffRequest(email="test@example.com", role="receptionist")
    assert req.email == "test@example.com"
    assert req.role == "receptionist"


def test_profile_update_schema():
    """Test ProfileUpdate schema."""
    update = ProfileUpdate(full_name="Updated Name", phone="+84123456789")
    assert update.full_name == "Updated Name"
    assert update.phone == "+84123456789"
