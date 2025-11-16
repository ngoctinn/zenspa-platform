# ZenSpa Backend

Nền tảng backend cho hệ thống ZenSpa sử dụng FastAPI, Supabase, và Redis.

## Cài Đặt

### Yêu cầu hệ thống

- Python 3.12+
- PostgreSQL (Supabase)
- Redis

### Setup môi trường

1. **Clone repository và vào thư mục backend:**

   ```bash
   cd backend
   ```

2. **Tạo virtual environment:**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows: venv\Scripts\activate
   ```

3. **Cài đặt dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Cấu hình environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env với thông tin thực tế
   ```

5. **Khởi chạy Redis (local):**

   ```bash
   docker run -d -p 6379:6379 redis
   ```

6. **Khởi chạy ứng dụng:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

## Health Checks

- General: `GET /health`
- Database: `GET /health/db`
- Redis: `GET /health/redis`

## Cấu trúc dự án

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── core/                # Core modules (config, db, logging, etc.)
│   ├── common/              # Common schemas and helpers
│   ├── api/                 # API routers
│   ├── redis/               # Redis helpers
│   └── modules/             # Domain modules (appointment, customer, etc.)
├── alembic/                 # Database migrations
├── tests/                   # Unit and integration tests
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md
```

## Development

### Code Quality

- **Linting:** `ruff check .`
- **Formatting:** `black .`
- **Type checking:** `mypy .` (optional)

### Testing

```bash
pytest
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_config.py
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Environment Variables

| Variable                  | Description                  | Required             |
| ------------------------- | ---------------------------- | -------------------- |
| DATABASE_URL              | PostgreSQL connection string | Yes                  |
| UPSTASH_REDIS_REST_URL    | Upstash Redis REST API URL   | Yes                  |
| UPSTASH_REDIS_REST_TOKEN  | Upstash Redis REST API token | Yes                  |
| SUPABASE_URL              | Supabase project URL         | No (for future auth) |
| SUPABASE_ANON_KEY         | Supabase anonymous key       | No                   |
| SUPABASE_SERVICE_ROLE_KEY | Supabase service role key    | No                   |

## Contributing

1. Follow PEP 8 style guide
2. Use type hints
3. Write tests for new features
4. Update documentation
