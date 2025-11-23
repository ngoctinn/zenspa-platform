"""Xử lý exception và custom exceptions."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
from fastapi import status


class ErrorCode(str, Enum):
    """Mã lỗi để chuẩn hóa response lỗi."""

    # Lỗi client (4xx)
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"

    # Lỗi server (5xx)
    DATABASE_ERROR = "DATABASE_ERROR"
    CACHE_ERROR = "CACHE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


@dataclass
class ZenSpaException(Exception):
    """Exception cơ sở cho ứng dụng ZenSpa."""

    message: str
    code: ErrorCode
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    details: Dict[str, Any] | None = None


class DatabaseException(ZenSpaException):
    """Lỗi liên quan đến database."""

    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(
            message=message,
            code=ErrorCode.DATABASE_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details,
        )


class CacheException(ZenSpaException):
    """Lỗi liên quan đến cache."""

    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(
            message=message,
            code=ErrorCode.CACHE_ERROR,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details,
        )


class ValidationException(ZenSpaException):
    """Lỗi validation."""

    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class NotFoundException(ZenSpaException):
    """Lỗi tài nguyên không tìm thấy."""

    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(
            message=message,
            code=ErrorCode.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


# Exception handlers cho FastAPI
from datetime import datetime, timezone
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.logging import logger


async def zenspa_exception_handler(
    request: Request, exc: ZenSpaException
) -> JSONResponse:
    """Xử lý custom ZenSpa exceptions."""
    # Ghi log lỗi
    logger.error(
        f"ZenSpaException: {exc.message}",
        extra={
            "request_id": getattr(request.state, "request_id", None),
            "error_code": exc.code,
            "status_code": exc.status_code,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": getattr(request.state, "request_id", None),
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Xử lý lỗi validation Pydantic."""
    # Ghi log lỗi
    logger.error(
        f"ValidationError: {exc.errors()}",
        extra={"request_id": getattr(request.state, "request_id", None)},
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Dữ liệu đầu vào không hợp lệ",
                "details": exc.errors(),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": getattr(request.state, "request_id", None),
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Xử lý catch-all cho unexpected exceptions."""
    # Ghi log full exception để debug
    logger.exception(
        f"Unhandled exception: {exc}",
        extra={"request_id": getattr(request.state, "request_id", None)},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Đã xảy ra lỗi không mong muốn",
                # Không expose chi tiết exception trong production
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": getattr(request.state, "request_id", None),
        },
    )
