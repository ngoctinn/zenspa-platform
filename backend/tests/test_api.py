"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test general health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "service" in data
    assert "version" in data


def test_health_db_endpoint(client):
    """Test database health endpoint."""
    response = client.get("/health/db")

    # Should return 200 or 503 depending on DB availability
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "connected" in data
    assert "response_time_ms" in data


def test_health_redis_endpoint(client):
    """Test Redis health endpoint."""
    response = client.get("/health/redis")

    # Should return 200 or 503 depending on Redis availability
    assert response.status_code in [200, 503]
    data = response.json()
    assert "status" in data
    assert "redis" in data
    assert "connected" in data
    assert "response_time_ms" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data


def test_ping_endpoint(client):
    """Test ping endpoint."""
    response = client.get("/ping")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pong"
