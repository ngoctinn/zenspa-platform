"""Tests for database layer."""

import pytest
from unittest.mock import patch, MagicMock
from app.core.database import check_database_health
from app.core.exceptions import DatabaseException


def test_check_database_health_success():
    """Test successful database health check."""
    with patch('app.core.database.engine') as mock_engine:
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_conn.execute.return_value = None

        is_healthy, response_time = check_database_health()

        assert is_healthy is True
        assert response_time >= 0


def test_check_database_health_failure():
    """Test failed database health check."""
    with patch('app.core.database.engine') as mock_engine:
        mock_engine.connect.side_effect = Exception("Connection failed")

        is_healthy, response_time = check_database_health()

        assert is_healthy is False
        assert response_time >= 0
