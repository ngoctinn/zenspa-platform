"""Tests for database layer (Async)."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from app.core.database import check_database_health
from app.core.exceptions import DatabaseException


@pytest.mark.asyncio
async def test_check_database_health_success():
    """Test successful database health check."""
    with patch("app.core.database.engine") as mock_engine:
        # Mock async connection context manager
        mock_conn = AsyncMock()
        mock_engine.connect.return_value.__aenter__.return_value = mock_conn
        mock_conn.execute.return_value = None

        is_healthy, response_time = await check_database_health()

        assert is_healthy is True
        assert response_time >= 0


@pytest.mark.asyncio
async def test_check_database_health_failure():
    """Test failed database health check."""
    with patch("app.core.database.engine") as mock_engine:
        # Mock async connection failure
        mock_engine.connect.side_effect = Exception("Connection failed")

        is_healthy, response_time = await check_database_health()

        assert is_healthy is False
        assert response_time >= 0
