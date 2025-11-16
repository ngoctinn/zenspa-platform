# Hướng Dẫn Thiết Lập Backend ZenSpa Platform

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập môi trường phát triển cục bộ cho backend của ZenSpa Platform. Backend được xây dựng bằng FastAPI với SQLModel (sync), Redis, và PostgreSQL thông qua Supabase.

Sau khi hoàn thành, bạn sẽ có một server backend chạy trên `http://localhost:8000` với các endpoint health check và sẵn sàng cho việc phát triển các module domain.

## Yêu Cầu Hệ Thống

### Phần Mềm Cần Thiết

- **Python 3.12+**: Backend sử dụng các tính năng mới nhất của Python
- **Git**: Để clone repository và quản lý version control
- **PostgreSQL**: Cơ sở dữ liệu chính (thông qua Supabase)
- **Redis**: Cho caching và session (thông qua Redis Cloud)

### Tài Khoản Và Dịch Vụ

- Tài khoản Supabase (cho PostgreSQL database)
- Tài khoản Redis Cloud (cho Redis instance)
- (Tùy chọn) Tài khoản GitHub để push code

## Bước 1: Chuẩn Bị Môi Trường

### 1.1 Cài Đặt Python 3.12+

```bash
# Kiểm tra version Python hiện tại
python --version

# Nếu chưa có Python 3.12+, tải từ https://python.org
# Hoặc sử dụng pyenv trên Linux/Mac
```

### 1.2 Clone Repository

```bash
git clone https://github.com/ngoctinn/zenspa-platform.git
cd zenspa-platform
```

### 1.3 Tạo Virtual Environment

```bash
# Trong thư mục backend
cd backend

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

## Bước 2: Cài Đặt Dependencies

### 2.1 Cài Đặt Python Packages

```bash
pip install -r requirements.txt
```

### 2.2 Xác Minh Cài Đặt

```bash
# Kiểm tra các package chính
python -c "import fastapi, sqlmodel, redis, alembic; print('All dependencies installed successfully')"
```

## Bước 3: Thiết Lập Cơ Sở Dữ Liệu

### 3.1 Tạo Tài Khoản Supabase

1. Truy cập [supabase.com](https://supabase.com)
2. Tạo project mới
3. Lấy connection string từ Settings > Database

### 3.2 Tạo Tài Khoản Redis Cloud

1. Truy cập [redis.com](https://redis.com)
2. Tạo free tier instance
3. Lấy connection URL

### 3.3 Cấu Hình Environment Variables

```bash
# Copy file mẫu
cp .env.example .env

# Chỉnh sửa .env với thông tin thực tế
# Sử dụng editor yêu thích
code .env
```

Nội dung file `.env` cần thiết:

```env
# Database
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres

# Redis
REDIS_URL=redis://:[password]@[host]:[port]

# Application
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Bước 4: Thiết Lập Database Schema

### 4.1 Chạy Migration Ban Đầu

```bash
# Đảm bảo đang trong thư mục backend
cd backend

# Kích hoạt virtual environment nếu chưa
venv\Scripts\activate  # Windows

# Chạy migration
alembic upgrade head
```

### 4.2 Xác Minh Database Connection

```bash
# Kiểm tra kết nối database
python -c "from app.core.database import check_database_health; print('Database health:', check_database_health())"
```

## Bước 5: Chạy Application

### 5.1 Khởi Động Server

```bash
# Từ thư mục backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5.2 Xác Minh Server Đang Chạy

Mở browser và truy cập:

- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## Bước 6: Chạy Tests

### 6.1 Thiết Lập Environment Cho Tests

```bash
# Đảm bảo .env được cấu hình đúng
# Tạo database test riêng nếu cần
```

### 6.2 Chạy Test Suite

```bash
# Từ thư mục backend
pytest tests/ -v --cov=app --cov-report=html
```

### 6.3 Xem Coverage Report

Mở file `htmlcov/index.html` trong browser để xem báo cáo coverage.

## Xử Lý Sự Cố Thường Gặp

### Lỗi Database Connection

```
sqlalchemy.exc.OperationalError: connection failed
```

**Giải pháp**:

- Kiểm tra DATABASE_URL trong .env
- Đảm bảo Supabase project đang active
- Kiểm tra firewall và network connection

### Lỗi Redis Connection

```
redis.exceptions.ConnectionError: Connection refused
```

**Giải pháp**:

- Kiểm tra REDIS_URL trong .env
- Đảm bảo Redis instance đang running
- Kiểm tra credentials

### Lỗi Import Module

```
ModuleNotFoundError: No module named 'xyz'
```

**Giải pháp**:

- Đảm bảo virtual environment được kích hoạt
- Chạy lại `pip install -r requirements.txt`
- Kiểm tra Python version (cần 3.12+)

### Port 8000 Đã Được Sử Dụng

```
OSError: [Errno 48] Address already in use
```

**Giải pháp**:

- Thay đổi port: `uvicorn app.main:app --reload --port 8001`
- Hoặc kill process đang dùng port 8000

## Cấu Trúc Thư Mục Quan Trọng

```
backend/
├── app/
│   ├── main.py              # Entry point FastAPI app
│   ├── core/                # Core functionality
│   │   ├── config.py        # Settings và configuration
│   │   ├── database.py      # Database connection
│   │   └── ...
│   ├── api/                 # API endpoints
│   └── modules/             # Domain modules (sẽ thêm sau)
├── tests/                   # Unit và integration tests
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
└── .env.example             # Environment template
```

## Tiếp Theo

Sau khi thiết lập thành công:

1. Đọc tài liệu design trong `docs/ai/design/feature-backend-foundation.md`
2. Bắt đầu phát triển module đầu tiên (ví dụ: auth module)
3. Tham khảo planning trong `docs/ai/planning/` để biết thứ tự ưu tiên

## Liên Hệ Hỗ Trợ

Nếu gặp vấn đề trong quá trình thiết lập:

- Kiểm tra logs của application
- Tham khảo `backend/README.md` cho thông tin chi tiết hơn
- Tạo issue trên GitHub repository nếu cần hỗ trợ từ team

---

**Version**: 1.0
**Last Updated**: November 16, 2025
**Authors**: ZenSpa Development Team
