"""Tests for exception handling."""

import pytest
from fastapi import status
from app.core.exceptions import (
    ZenSpaException,
    DatabaseException,
    ValidationException,
    NotFoundException,
    ErrorCode
)


def test_zenspa_exception_creation():
    """Test ZenSpaException creation."""
    exc = ZenSpaException(
        message="Test error",
        code=ErrorCode.INTERNAL_ERROR,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details={"key": "value"}
    )

    assert exc.message == "Test error"
    assert exc.code == ErrorCode.INTERNAL_ERROR
    assert exc.status_code == 500
    assert exc.details == {"key": "value"}


def test_database_exception():
    """Test DatabaseException."""
    exc = DatabaseException("Database connection failed")

    assert exc.code == ErrorCode.DATABASE_ERROR
    assert exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


def test_validation_exception():
    """Test ValidationException."""
    exc = ValidationException("Invalid input")

    assert exc.code == ErrorCode.VALIDATION_ERROR
    assert exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_not_found_exception():
    """Test NotFoundException."""
    exc = NotFoundException("Resource not found")

    assert exc.code == ErrorCode.NOT_FOUND
    assert exc.status_code == status.HTTP_404_NOT_FOUND
