"""
Custom exceptions and error codes for the application.
"""

from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """Standardized error codes."""

    # System errors (1xxx)
    INTERNAL_SERVER_ERROR = "ERR_1000"
    SERVICE_UNAVAILABLE = "ERR_1001"
    CONFIGURATION_ERROR = "ERR_1002"

    # Database errors (2xxx)
    DATABASE_CONNECTION_ERROR = "ERR_2000"
    DATABASE_QUERY_ERROR = "ERR_2001"
    DATABASE_TRANSACTION_ERROR = "ERR_2002"
    RECORD_NOT_FOUND = "ERR_2003"
    DUPLICATE_RECORD = "ERR_2004"

    # Redis errors (3xxx)
    REDIS_CONNECTION_ERROR = "ERR_3000"
    REDIS_OPERATION_ERROR = "ERR_3001"

    # Validation errors (4xxx)
    VALIDATION_ERROR = "ERR_4000"
    INVALID_INPUT = "ERR_4001"
    MISSING_FIELD = "ERR_4002"

    # Authentication/Authorization errors (5xxx)
    UNAUTHORIZED = "ERR_5000"
    FORBIDDEN = "ERR_5001"
    INVALID_TOKEN = "ERR_5002"
    TOKEN_EXPIRED = "ERR_5003"

    # Business logic errors (6xxx)
    BUSINESS_RULE_VIOLATION = "ERR_6000"
    OPERATION_NOT_ALLOWED = "ERR_6001"


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseException(AppException):
    """Database-related exceptions."""

    def __init__(
        self,
        message: str = "Database error occurred",
        error_code: ErrorCode = ErrorCode.DATABASE_CONNECTION_ERROR,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500,
            details=details,
        )


class RedisException(AppException):
    """Redis-related exceptions."""

    def __init__(
        self,
        message: str = "Redis error occurred",
        error_code: ErrorCode = ErrorCode.REDIS_CONNECTION_ERROR,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=500,
            details=details,
        )


class ValidationException(AppException):
    """Validation-related exceptions."""

    def __init__(
        self,
        message: str = "Validation error",
        error_code: ErrorCode = ErrorCode.VALIDATION_ERROR,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details,
        )


class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(
        self,
        message: str = "Resource not found",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            error_code=ErrorCode.RECORD_NOT_FOUND,
            status_code=404,
            details=details,
        )


class UnauthorizedException(AppException):
    """Unauthorized access exception."""

    def __init__(
        self,
        message: str = "Unauthorized access",
        error_code: ErrorCode = ErrorCode.UNAUTHORIZED,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            details=details,
        )


class ForbiddenException(AppException):
    """Forbidden access exception."""

    def __init__(
        self,
        message: str = "Access forbidden",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            error_code=ErrorCode.FORBIDDEN,
            status_code=403,
            details=details,
        )
