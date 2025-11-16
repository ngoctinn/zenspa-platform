"""Common Pydantic schemas dùng chung trong ứng dụng."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Response model cho health check endpoints."""

    status: str  # "healthy" | "unhealthy"
    timestamp: datetime
    service: str
    version: str


class DatabaseHealthResponse(HealthCheckResponse):
    """Response model cho database health check."""

    database: str
    connected: bool
    response_time_ms: float


class RedisHealthResponse(HealthCheckResponse):
    """Response model cho Redis health check."""

    redis: str
    connected: bool
    response_time_ms: float


class ErrorDetail(BaseModel):
    """Model chi tiết lỗi."""

    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Model response lỗi chuẩn."""

    status: str = "error"
    error: ErrorDetail
    timestamp: datetime
    request_id: Optional[str] = None


class SuccessResponse(BaseModel):
    """Model response thành công chuẩn."""

    status: str = "success"
    data: Any
    message: Optional[str] = None
    timestamp: Optional[datetime] = None


class PaginationMeta(BaseModel):
    """Metadata phân trang."""

    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(SuccessResponse):
    """Model response phân trang."""

    data: List[Any]
    meta: PaginationMeta


class BaseFilter(BaseModel):
    """Model filter cơ sở cho list endpoints."""

    page: int = 1
    page_size: int = 10
    sort_by: Optional[str] = None
    sort_order: str = "asc"  # "asc" | "desc"


class BaseCreateRequest(BaseModel):
    """Model cơ sở cho create requests."""

    pass


class BaseUpdateRequest(BaseModel):
    """Model cơ sở cho update requests."""

    pass
