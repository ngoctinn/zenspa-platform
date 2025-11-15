# ZenSpa Backend

Backend foundation cho hệ thống quản lý spa, sử dụng FastAPI, PostgreSQL (Supabase), và Redis.

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Python**: 3.12+
- **Database**: PostgreSQL 17+ (Supabase) với SQLModel (async)
- **Cache**: Redis 5.2.0
- **Migration**: Alembic 1.14.0
- **Logging**: python-json-logger (structured logging)
- **Retry**: tenacity (resilience patterns)

## Kiến trúc

```
backend/
├── app/
│   ├── core/          # Config, database, security, exceptions, logging
│   ├── common/        # Shared schemas and utilities
│   ├── api/           # API routers
│   ├── redis/         # Redis client and helpers
│   └── modules/       # Domain modules (future)
├── tests/             # Test suites
├── alembic/           # Database migrations
└── requirements.txt   # Dependencies
```

## Setup

### 1. Tạo virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình environment

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Cập nhật các giá trị trong `.env`:

- `DATABASE_URL`: Connection string của Supabase PostgreSQL
- `REDIS_HOST`, `REDIS_PORT`: Redis configuration
- `SECRET_KEY`: Secret key cho security (generate mới cho production)
- `CORS_ORIGINS`: Frontend URLs cho CORS

### 4. Chạy database migrations

```bash
alembic upgrade head
```

### 5. Chạy development server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Health Check Endpoints

- `GET /api/v1/health` - Overall health status
- `GET /api/v1/health/db` - Database connection health
- `GET /api/v1/health/redis` - Redis connection health

## Testing

Chạy toàn bộ tests:

```bash
pytest
```

Chạy với coverage report:

```bash
pytest --cov=app --cov-report=html
```

## Documentation

- API Documentation: http://localhost:8000/docs (Swagger UI)
- Alternative API Documentation: http://localhost:8000/redoc (ReDoc)
- OpenAPI Schema: http://localhost:8000/openapi.json

## Security Features

- Security headers middleware (HSTS, X-Frame-Options, etc.)
- Request ID tracking (UUID per request)
- Standardized error responses with error codes
- Environment-based configuration
- Input validation với Pydantic

## Logging

- Structured JSON logging cho production
- Request ID propagation trong logs
- Configurable log levels via `LOG_LEVEL` environment variable

## Error Handling

- Standardized ErrorResponse format
- ErrorCode enum cho consistent error codes
- Global exception handlers
- HTTP status mapping

## Performance

- Async/await patterns throughout
- Database connection pooling (min 5, max 20)
- Redis caching với graceful fallback
- Retry mechanisms cho database operations
- Request timeout: 30s

## Contributing

Xem tài liệu trong `docs/ai/implementation/feature-backend-foundation.md` để biết chi tiết implementation guidelines.

## License

Proprietary - ZenSpa Platform
