# Quick Start Guide

## 1. Cài đặt dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## 2. Cấu hình môi trường

File `.env` đã được tạo sẵn với cấu hình development.

**Quan trọng**: Cập nhật `DATABASE_URL` trong `.env` với connection string của Supabase PostgreSQL:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
```

## 3. Chạy application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4. Test health check endpoints

Sau khi server chạy, test các endpoints:

```bash
# Overall health
curl http://localhost:8000/api/v1/health

# Database health
curl http://localhost:8000/api/v1/health/db

# Redis health
curl http://localhost:8000/api/v1/health/redis
```

## 5. Xem API documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Lưu ý

- **Redis không bắt buộc**: Application sẽ chạy gracefully ngay cả khi Redis không available
- **Database bắt buộc**: Cần có PostgreSQL connection để application start
- Nếu chưa có Supabase database, có thể dùng local PostgreSQL:

  ```bash
  # Install PostgreSQL locally
  # Create database
  createdb zenspa_db

  # Update .env
  DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/zenspa_db
  ```

## Next Steps

Sau khi backend foundation hoạt động, có thể:

1. Chạy tests (Task 4.1-4.4)
2. Tạo database migrations với Alembic
3. Phát triển domain modules trong `app/modules/`
