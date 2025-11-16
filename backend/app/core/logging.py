"""Cấu hình logging cho ứng dụng."""

import logging
import json
import sys
from datetime import datetime
from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """Format log dưới dạng JSON cho structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record thành JSON."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Thêm request_id nếu có
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        # Thêm exception info nếu có
        if record.exc_info:
            log_data["exception"] = str(record.exc_info[1])

        return json.dumps(log_data)


def setup_logging() -> None:
    """Thiết lập cấu hình logging dựa trên environment."""
    # Lấy log level từ settings
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Tạo formatter dựa trên environment
    if settings.environment == "production":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # Cấu hình handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    # Cấu hình root logger
    logging.basicConfig(
        level=log_level, handlers=[handler], force=True  # Ghi đè cấu hình hiện có
    )

    # Giảm noise từ external libraries
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.INFO)

    # Log thông điệp khởi động
    logger = logging.getLogger(__name__)
    logger.info(
        f"Logging đã cấu hình cho {settings.environment} environment với level {settings.log_level}"
    )


# Instance logger toàn cục
logger = logging.getLogger(__name__)
