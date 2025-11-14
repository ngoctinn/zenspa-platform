---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
feature: backend-foundation
---

# Hướng Dẫn Triển Khai - Nền Tảng Backend

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

### Điều Kiện Tiên Quyết

- Python 3.12 hoặc cao hơn
- pip (Python package manager)
- Git
- Redis server (local hoặc cloud)
- Supabase project credentials

### Các Bước Thiết Lập Môi Trường

```bash
# 1. Di chuyển vào thư mục backend
cd backend

# 2. Tạo virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Cài đặt dependencies
pip install -r requirements.txt

# 6. Copy environment template
cp .env.example .env

# 7. Điền thông tin vào .env
# Mở .env và điền các giá trị cần thiết

# 8. Chạy backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Cấu Hình Cần Thiết

**File `.env` cần có:**

```env
# Application
APP_NAME=ZenSpa Backend
APP_VERSION=0.1.0
DEBUG=True
ENVIRONMENT=development

# Server
HOST=0.0.0.0
PORT=8000

# CORS - Thêm origins cần thiết, phân cách bằng dấu phẩy
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_ECHO=False

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_DECODE_RESPONSES=True

# Logging
LOG_LEVEL=INFO
```

### Setup Redis Local (Docker)

```bash
# Pull và chạy Redis container
docker run -d \
  --name zenspa-redis \
  -p 6379:6379 \
  redis:7-alpine

# Verify Redis đang chạy
docker ps | grep zenspa-redis

# Test connection
redis-cli ping
# Response: PONG
```

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

### Cấu Trúc Thư Mục Chi Tiết

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── core/                   # Core configurations và utilities
│   │   ├── __init__.py
│   │   ├── config.py          # Settings với Pydantic
│   │   ├── database.py        # Database engine và session
│   │   ├── logging.py         # Logging configuration
│   │   ├── exceptions.py      # Custom exceptions và handlers
│   │   └── security.py        # Security utilities (future)
│   │
│   ├── common/                 # Shared components
│   │   ├── __init__.py
│   │   ├── schemas.py         # Common Pydantic schemas
│   │   ├── helpers.py         # Utility functions
│   │   └── constants.py       # Constants và enums
│   │
│   ├── redis/                  # Redis layer
│   │   ├── __init__.py
│   │   ├── client.py          # Redis connection
│   │   └── helpers.py         # Cache helpers
│   │
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── api_v1.py          # API router aggregation
│   │   └── health.py          # Health check endpoints
│   │
│   └── modules/                # Domain modules (empty for now)
│       └── __init__.py
│
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_redis.py
│   └── test_health.py
│
├── .env                        # Environment variables (gitignored)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # Setup instructions
```

### Quy Ước Đặt Tên

- **Files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions/Variables:** `snake_case`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private members:** `_leading_underscore`
- **Module files:** `{domain}-{type}.py` (cho modules)

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### 1. Configuration Management (`app/core/config.py`)

```python
"""
Configuration management sử dụng Pydantic Settings.
Settings object là singleton, load một lần khi import.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    """
    Application settings loaded từ environment variables.
    Tất cả values được validate khi load.
    """

    # Application
    APP_NAME: str = "ZenSpa Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS - Parse comma-separated origins
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Convert comma-separated string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Database (Supabase PostgreSQL)
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_ECHO: bool = False

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_DECODE_RESPONSES: bool = True

    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env
    )

# Singleton instance
settings = Settings()
```

**Usage:**

```python
from app.core.config import settings

print(settings.DATABASE_URL)
print(settings.cors_origins_list)
```

### 2. Database Layer (`app/core/database.py`)

```python
"""
Async database connection với SQLAlchemy.
Sử dụng connection pooling cho performance.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from app.core.config import settings
import time

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Verify connections before using
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_async_session():
    """
    Dependency để get database session.

    Usage trong endpoint:
        @router.get("/")
        async def endpoint(db: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def check_database_health() -> tuple[bool, float]:
    """
    Kiểm tra database health và measure response time.

    Returns:
        tuple[bool, float]: (is_healthy, response_time_ms)
    """
    try:
        start_time = time.time()
        async with AsyncSessionLocal() as session:
            # Simple query to check connection
            await session.execute(text("SELECT 1"))
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        return True, response_time
    except Exception as e:
        # Log error
        return False, 0.0

async def init_db() -> None:
    """
    Initialize database connection.
    Gọi trong startup event.
    """
    try:
        async with engine.begin() as conn:
            # Test connection
            await conn.execute(text("SELECT 1"))
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise

async def close_db() -> None:
    """
    Close database connections.
    Gọi trong shutdown event.
    """
    await engine.dispose()
    print("✅ Database connections closed")
```

### 3. Redis Layer (`app/redis/client.py`, `app/redis/helpers.py`)

**`app/redis/client.py`:**

```python
"""
Redis connection management.
"""

from redis import asyncio as aioredis
from app.core.config import settings
import time

# Redis client (will be initialized in startup event)
redis_client: aioredis.Redis | None = None

async def get_redis_client() -> aioredis.Redis:
    """
    Get Redis client instance.

    Usage:
        redis = await get_redis_client()
        await redis.set("key", "value")
    """
    if redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return redis_client

async def init_redis() -> None:
    """
    Initialize Redis connection.
    Gọi trong startup event.
    """
    global redis_client
    try:
        redis_client = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD,
            decode_responses=settings.REDIS_DECODE_RESPONSES,
            encoding="utf-8",
        )
        # Test connection
        await redis_client.ping()
        print("✅ Redis connected successfully")
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("⚠️  App will continue without Redis")
        redis_client = None

async def close_redis() -> None:
    """
    Close Redis connection.
    Gọi trong shutdown event.
    """
    global redis_client
    if redis_client:
        await redis_client.close()
        print("✅ Redis connection closed")

async def check_redis_health() -> tuple[bool, float]:
    """
    Kiểm tra Redis health và measure response time.

    Returns:
        tuple[bool, float]: (is_healthy, response_time_ms)
    """
    if redis_client is None:
        return False, 0.0

    try:
        start_time = time.time()
        await redis_client.ping()
        response_time = (time.time() - start_time) * 1000
        return True, response_time
    except Exception:
        return False, 0.0
```

**`app/redis/helpers.py`:**

```python
"""
Redis helper functions cho caching.
"""

from typing import Any
import json
from app.redis.client import get_redis_client

async def cache_get(key: str) -> Any | None:
    """
    Get value từ cache.

    Args:
        key: Cache key

    Returns:
        Cached value hoặc None nếu không tồn tại
    """
    try:
        redis = await get_redis_client()
        value = await redis.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception:
        return None

async def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Set value vào cache với TTL.

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (default 1 hour)

    Returns:
        True nếu thành công, False nếu fail
    """
    try:
        redis = await get_redis_client()
        await redis.setex(key, ttl, json.dumps(value))
        return True
    except Exception:
        return False

async def cache_delete(key: str) -> bool:
    """
    Delete key từ cache.

    Args:
        key: Cache key

    Returns:
        True nếu thành công
    """
    try:
        redis = await get_redis_client()
        await redis.delete(key)
        return True
    except Exception:
        return False
```

### 4. Exception Handling (`app/core/exceptions.py`)

```python
"""
Custom exceptions và exception handlers.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from datetime import datetime

# Custom Exceptions
class ZenSpaException(Exception):
    """Base exception cho ZenSpa"""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class DatabaseException(ZenSpaException):
    """Database related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")

class CacheException(ZenSpaException):
    """Cache related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, "CACHE_ERROR")

class ValidationException(ZenSpaException):
    """Validation exceptions"""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")

# Exception Handlers
async def zenspa_exception_handler(request: Request, exc: ZenSpaException):
    """Handler cho ZenSpaException"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )

async def validation_exception_handler(request: Request, exc: Exception):
    """Handler cho validation errors từ Pydantic"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": str(exc),
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handler cho uncaught exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
            "timestamp": datetime.utcnow().isoformat(),
        },
    )
```

### 5. Logging Setup (`app/core/logging.py`)

```python
"""
Logging configuration.
"""

import logging
import sys
from app.core.config import settings

def setup_logging():
    """
    Setup logging với custom format.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper())

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Giảm noise từ external libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Call khi import
setup_logging()
```

### 6. Common Schemas (`app/common/schemas.py`)

```python
"""
Common Pydantic schemas dùng chung.
"""

from pydantic import BaseModel
from datetime import datetime

class HealthCheckResponse(BaseModel):
    """Base health check response"""
    status: str  # "healthy" | "unhealthy"
    timestamp: datetime
    service: str
    version: str

class DatabaseHealthResponse(HealthCheckResponse):
    """Database health check response"""
    database: str
    connected: bool
    response_time_ms: float

class RedisHealthResponse(HealthCheckResponse):
    """Redis health check response"""
    redis: str
    connected: bool
    response_time_ms: float
```

### 7. Health Check Endpoints (`app/api/health.py`)

```python
"""
Health check endpoints.
"""

from fastapi import APIRouter, status
from datetime import datetime
from app.common.schemas import (
    HealthCheckResponse,
    DatabaseHealthResponse,
    RedisHealthResponse,
)
from app.core.config import settings
from app.core.database import check_database_health
from app.redis.client import check_redis_health

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=HealthCheckResponse)
async def health_check():
    """
    Kiểm tra trạng thái tổng quan của hệ thống.
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
    )

@router.get("/db", response_model=DatabaseHealthResponse)
async def database_health_check():
    """
    Kiểm tra kết nối PostgreSQL database.
    """
    is_healthy, response_time = await check_database_health()

    return DatabaseHealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        timestamp=datetime.utcnow(),
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        database="postgresql",
        connected=is_healthy,
        response_time_ms=response_time,
    )

@router.get("/redis", response_model=RedisHealthResponse)
async def redis_health_check():
    """
    Kiểm tra kết nối Redis cache.
    """
    is_healthy, response_time = await check_redis_health()

    return RedisHealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        timestamp=datetime.utcnow(),
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        redis=f"{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        connected=is_healthy,
        response_time_ms=response_time,
    )
```

### 8. API Router (`app/api/api_v1.py`)

```python
"""
API v1 router aggregation.
"""

from fastapi import APIRouter
from app.api import health

# Create API v1 router
api_router = APIRouter(prefix="/api/v1")

# Include health check router
api_router.include_router(health.router)

# Future: Include domain module routers here
# api_router.include_router(appointment.router)
# api_router.include_router(customer.router)
```

### 9. Main Application (`app/main.py`)

```python
"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import (
    ZenSpaException,
    zenspa_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)
from app.core.database import init_db, close_db
from app.redis.client import init_redis, close_redis
from app.api.api_v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events.
    Startup: Initialize connections
    Shutdown: Close connections
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    await init_db()
    await init_redis()
    print(f"✅ {settings.APP_NAME} started successfully")

    yield

    # Shutdown
    print(f"🛑 Shutting down {settings.APP_NAME}")
    await close_db()
    await close_redis()
    print(f"✅ {settings.APP_NAME} stopped")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API cho hệ thống ZenSpa",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(ZenSpaException, zenspa_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(api_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }
```

## Mẫu & Thực Tiễn Tốt Nhất

### Async/Await Pattern

```python
# ✅ Good - Async all the way
@router.get("/items")
async def get_items(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Item))
    return result.scalars().all()

# ❌ Bad - Mixing sync and async
@router.get("/items")
def get_items():  # Missing async
    # Will block event loop
    pass
```

### Dependency Injection

```python
# ✅ Good - Use FastAPI dependencies
from fastapi import Depends

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token logic
    return user

@router.get("/me")
async def get_me(user = Depends(get_current_user)):
    return user
```

### Error Handling

```python
# ✅ Good - Specific exceptions
from app.core.exceptions import DatabaseException

async def get_user(user_id: int):
    try:
        # Database operation
        pass
    except SQLAlchemyError as e:
        raise DatabaseException(f"Failed to fetch user: {e}")

# ❌ Bad - Generic exceptions
async def get_user(user_id: int):
    try:
        pass
    except Exception as e:
        raise Exception("Error")  # Not informative
```

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

### Cơ Chế Retry

```python
# For database connection in init_db()
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def init_db():
    # Connection logic
    pass
```

### Graceful Degradation

```python
# Redis optional - app vẫn chạy khi Redis down
async def init_redis():
    try:
        # Redis connection
        pass
    except Exception as e:
        logger.warning(f"Redis unavailable: {e}")
        # Don't raise - app continues without Redis
```

## Cân Nhắc Hiệu Suất

### Connection Pooling

- Database: Pool size 10, max overflow 10
- Redis: Connection reuse
- Async operations để không block event loop

### Caching Strategy

```python
# Cache expensive queries
from app.redis.helpers import cache_get, cache_set

async def get_user(user_id: int):
    # Try cache first
    cached = await cache_get(f"user:{user_id}")
    if cached:
        return cached

    # Fetch from DB
    user = await db_fetch_user(user_id)

    # Cache for 1 hour
    await cache_set(f"user:{user_id}", user, ttl=3600)
    return user
```

## Ghi Chú Bảo Mật

### Environment Variables

- ✅ Không hardcode credentials
- ✅ Use `.env` file (gitignored)
- ✅ Validate khi startup
- ❌ Không log sensitive data

### CORS Configuration

```python
# ✅ Whitelist specific origins
CORS_ORIGINS=http://localhost:3000,https://app.zenspa.com

# ❌ KHÔNG dùng wildcard trong production
CORS_ORIGINS=*  # Insecure!
```

### Error Messages

```python
# ✅ User-friendly message
return {"error": "Invalid credentials"}

# ❌ Don't expose internals
return {"error": f"Database connection failed: {connection_string}"}
```
