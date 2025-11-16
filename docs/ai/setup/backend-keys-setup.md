# Hướng Dẫn Thiết Lập Keys và Dịch Vụ Cho Backend ZenSpa

## Tổng Quan

Hướng dẫn này sẽ giúp bạn lấy các API keys và thiết lập các dịch vụ bên thứ ba cần thiết cho backend ZenSpa Platform:

- **Supabase**: Cơ sở dữ liệu PostgreSQL và xác thực
- **Redis Upstash**: Caching và session storage

Sau khi hoàn thành, bạn sẽ có đầy đủ credentials để cấu hình file `.env` và chạy backend thành công.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản email hợp lệ
- Trình duyệt web
- Kết nối internet ổn định
- (Tùy chọn) Tài khoản GitHub để theo dõi repository

---

## Bước 1: Thiết Lập Supabase

### 1.1 Tạo Tài Khoản Supabase

1. Truy cập [supabase.com](https://supabase.com)
2. Click **"Start your project"** hoặc **"Sign Up"**
3. Đăng ký bằng email hoặc tài khoản Google/GitHub
4. Xác nhận email nếu cần

### 1.2 Tạo Project Mới

1. Sau khi đăng nhập, click **"New project"**
2. Điền thông tin project:
   - **Name**: `zenspa-platform` (hoặc tên tùy chọn)
   - **Database Password**: Tạo mật khẩu mạnh (ghi nhớ để dùng sau)
   - **Region**: Chọn region gần nhất (e.g., Singapore, Tokyo)
3. Click **"Create new project"**
4. Chờ project khởi tạo (khoảng 2-5 phút)

### 1.3 Lấy Database Credentials

1. Trong dashboard project, chọn tab **"Settings"** > **"Database"**
2. Copy các thông tin sau:

   - **Host**: `db.[project-ref].supabase.co`
   - **Database name**: `postgres`
   - **Port**: `5432`
   - **Username**: `postgres`
   - **Password**: Mật khẩu bạn đã tạo

3. Tạo connection string:
   ```
   postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres
   ```

### 1.4 Lấy API Keys

1. Trong dashboard, chọn tab **"Settings"** > **"API"**
2. Copy các keys:
   - **anon public**: Key công khai cho client-side
   - **service_role**: Key riêng tư cho server-side (cẩn thận bảo mật!)

**Quan trọng:** Chỉ dùng `service_role` key trong backend, không expose ra client.

### 1.5 Cấu Hình Database (Tùy Chọn)

1. Chọn tab **"SQL Editor"**
2. Chạy các lệnh cơ bản để test connection:
   ```sql
   SELECT version();
   CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);
   DROP TABLE test;
   ```

---

## Bước 2: Thiết Lập Redis Upstash

### 2.1 Tạo Tài Khoản Upstash

1. Truy cập [upstash.com](https://upstash.com)
2. Click **"Sign Up"** hoặc **"Get Started"**
3. Đăng ký bằng email hoặc tài khoản GitHub
4. Xác nhận email

### 2.2 Tạo Redis Database

1. Sau đăng nhập, click **"Create Database"**
2. Điền thông tin:
   - **Name**: `zenspa-cache` (hoặc tên tùy chọn)
   - **Type**: Chọn **"Global Database"** (free tier) hoặc **"Regional"**
   - **Region**: Chọn region gần nhất
3. Click **"Create"**

### 2.3 Lấy Redis Connection Details

1. Trong dashboard database, chọn tab **"Connect"**
2. Copy thông tin **REST API**:
   - **UPSTASH_REDIS_REST_URL**: URL endpoint (vd: `https://electric-sculpin-37629.upstash.io`)
   - **UPSTASH_REDIS_REST_TOKEN**: API token (vd: `AZL9AAI...`)

**Lưu ý:** Backend ZenSpa dùng REST API thay vì Redis protocol để đơn giản hóa kết nối và không cần client library phức tạp.

### 2.4 Test Connection (Tùy Chọn)

1. Trong dashboard, chọn tab **"Console"**
2. Chạy lệnh test:
   ```
   SET test_key "Hello ZenSpa"
   GET test_key
   DEL test_key
   ```

---

## Bước 3: Cấu Hình File .env

### 3.1 Tạo/Cập Nhật File .env

Trong thư mục `backend/`, tạo hoặc chỉnh sửa file `.env`:

```env
# Database (Supabase)
DATABASE_URL=postgresql://postgres:your_password@db.your_project_ref.supabase.co:5432/postgres

# Redis (Upstash REST API)
UPSTASH_REDIS_REST_URL=https://your_rest_url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_rest_token

# Application
SECRET_KEY=your_random_secret_key_here
DEBUG=True

# Supabase (cho xác thực JWT)
SUPABASE_URL=https://your_project_ref.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

### 3.2 Tạo Secret Key

Tạo secret key ngẫu nhiên cho ứng dụng:

```bash
# Sử dụng Python để generate
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Hoặc dùng online tool như [random.org](https://www.random.org/strings/)

### 3.3 Bảo Mật Keys

- **Không commit** file `.env` vào Git
- Thêm `.env` vào `.gitignore`
- Sử dụng environment variables trong production
- Chia sẻ keys cẩn thận với team

---

## Bước 4: Xác Minh Thiết Lập

### 4.1 Test Database Connection

```bash
# Trong thư mục backend
cd backend

# Kích hoạt virtual environment
venv\Scripts\activate  # Windows

# Test connection
python -c "
from app.core.database import check_database_health
print('Database status:', check_database_health())
"
```

### 4.2 Test Redis Connection

```bash
# Test Redis
python -c "
from app.redis.client import get_redis_client
redis = get_redis_client()
redis.setex('test', 60, 'ok')
print('Redis value:', redis.get('test'))
redis.delete('test')
print('Redis OK')
"
```

### 4.3 Chạy Health Check

```bash
# Khởi động server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Truy cập:

- http://localhost:8000/health (overall health)
- http://localhost:8000/health/db (database)
- http://localhost:8000/health/redis (redis)

---

## Xử Lý Sự Cố Thường Gặp

### Supabase Connection Failed

```
FATAL: password authentication failed
```

**Giải pháp:**

- Kiểm tra DATABASE_URL trong .env
- Đảm bảo password đúng (không có ký tự đặc biệt gây lỗi)
- Kiểm tra project status trên Supabase dashboard

### Redis Connection Failed

```
requests.exceptions.RequestException: 401 Client Error
```

**Giải pháp:**

- Kiểm tra UPSTASH_REDIS_REST_URL và UPSTASH_REDIS_REST_TOKEN trong .env
- Đảm bảo token đúng và chưa expired
- Kiểm tra database Upstash đang active

### Invalid JWT Token

```
Invalid JWT: unable to decode
```

**Giải pháp:**

- Kiểm tra SUPABASE_URL và keys
- Đảm bảo dùng đúng anon key cho client, service_role cho server

### Database Migration Failed

```
alembic upgrade head
```

**Lỗi:** No such table
**Giải pháp:**

- Đảm bảo database trống trước khi chạy migration
- Hoặc reset database trên Supabase

---

## Chi Phí và Giới Hạn

### Supabase Free Tier

- **Database**: 500MB storage
- **Bandwidth**: 50MB/month
- **Users**: Unlimited (cho auth)
- **Upgrade**: Khi cần scale

### Upstash Free Tier

- **Database size**: 10MB
- **Requests**: 10,000/month
- **Connections**: 20 concurrent
- **Upgrade**: Khi cần performance cao

---

## Tài Nguyên Tham Khảo

- [Supabase Documentation](https://supabase.com/docs)
- [Upstash Redis Docs](https://docs.upstash.com/redis)
- [ZenSpa Backend README](../backend/README.md)
- [Environment Setup Guide](backend-setup.md)

---

**Version**: 1.0
**Last Updated**: November 16, 2025
**Authors**: ZenSpa Development Team
