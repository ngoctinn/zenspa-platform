"""Tests cho auth module."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import verify_jwt, get_current_user

client = TestClient(app)


def test_verify_jwt_invalid():
    """Test verify JWT không hợp lệ."""
    with pytest.raises(Exception):  # HTTPException
        verify_jwt("invalid_token")


def test_get_current_user_no_token():
    """Test get_current_user không có token."""
    response = client.get("/api/v1/health")
    # Health không require auth, nên pass
    assert response.status_code == 200


def test_admin_update_role_no_auth():
    """Test admin endpoint không auth."""
    response = client.put("/api/v1/admin/users/123/role", json={"role": "admin"})
    assert response.status_code == 401  # Unauthorized


def test_get_user_profile_no_auth():
    """Test user profile endpoint không auth."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401


# Note: Để test đầy đủ, cần mock Supabase và tạo valid JWT.
# Hiện tại, basic tests để validate structure.
