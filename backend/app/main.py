"""
Main FastAPI application.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.common.schemas import ErrorResponse
from app.core.config import settings
from app.core.database import db
from app.core.exceptions import AppException, ErrorCode
from app.core.logging import get_logger, setup_logging
from app.core.middleware import RequestIDMiddleware
from app.core.security import SecurityHeadersMiddleware
from app.redis.client import redis_client

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.app_name}...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    # Connect to database
    try:
        await db.connect()
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

    # Connect to Redis (non-critical, graceful degradation)
    await redis_client.connect()

    logger.info(f"{settings.app_name} started successfully")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.app_name}...")
    await db.disconnect()
    await redis_client.disconnect()
    logger.info(f"{settings.app_name} shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Backend foundation for ZenSpa platform",
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add middleware (order matters - executed bottom to top)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_methods_list,
    allow_headers=[settings.cors_allow_headers],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(api_router)


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions."""
    logger.error(
        f"Application error: {exc.error_code} - {exc.message}",
        extra={"details": exc.details},
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            error_code=ErrorCode.VALIDATION_ERROR,
            message="Request validation failed",
            details={"errors": exc.errors()},
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred",
            details={"error": str(exc)} if settings.debug else {},
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )


# Root endpoint
@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "service": settings.app_name,
        "version": settings.api_version,
        "status": "running",
    }
