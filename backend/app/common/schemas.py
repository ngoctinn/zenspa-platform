"""
Common response schemas for API endpoints.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from app.core.exceptions import ErrorCode

T = TypeVar("T")


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(..., description="Health status (healthy/unhealthy)")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")
    details: dict[str, Any] = Field(
        default_factory=dict, description="Additional details"
    )


class ErrorResponse(BaseModel):
    """Standardized error response schema."""

    error_code: ErrorCode = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: dict[str, Any] = Field(
        default_factory=dict, description="Additional error details"
    )
    request_id: str | None = Field(None, description="Request ID for tracking")


class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response wrapper."""

    success: bool = Field(True, description="Success status")
    data: T = Field(..., description="Response data")
    message: str | None = Field(None, description="Optional message")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""

    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

    @staticmethod
    def create(
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        """Create paginated response."""
        total_pages = (total + page_size - 1) // page_size
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
