"""
Structured logging configuration for the application.
Uses JSON logging in production, colored console logging in development.
"""

import logging
import sys
from contextvars import ContextVar
from typing import Any

from pythonjsonlogger import jsonlogger

from app.core.config import settings

# Context variable to store request ID
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


class JSONFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter that includes request ID."""

    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        """Add custom fields to log record."""
        super().add_fields(log_record, record, message_dict)

        # Add request ID if available
        request_id = request_id_var.get()
        if request_id:
            log_record["request_id"] = request_id

        # Add environment
        log_record["environment"] = settings.environment

        # Add service name
        log_record["service"] = settings.app_name


class ColoredFormatter(logging.Formatter):
    """Colored console formatter for development."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
        "RESET": "\033[0m",  # Reset
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Add request ID to record
        request_id = request_id_var.get()
        record.request_id = request_id or "N/A"  # type: ignore[attr-defined]

        # Add color
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )

        return super().format(record)


def setup_logging() -> None:
    """Configure application logging."""
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)

    # Use JSON formatter in production, colored formatter in development
    if settings.is_production:
        formatter = JSONFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        formatter = ColoredFormatter(
            "%(asctime)s [%(levelname)s] [%(request_id)s] %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Set third-party library log levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("redis").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get logger for given name."""
    return logging.getLogger(name)


def set_request_id(request_id: str) -> None:
    """Set request ID in context."""
    request_id_var.set(request_id)


def get_request_id() -> str | None:
    """Get request ID from context."""
    return request_id_var.get()
