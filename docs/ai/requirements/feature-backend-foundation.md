---
phase: requirements
title: Yêu Cầu & Hiểu Vấn Đề
description: Làm rõ không gian vấn đề, thu thập yêu cầu và xác định tiêu chí thành công
feature: backend-foundation
---

# Yêu Cầu & Hiểu Vấn Đề - Nền Tảng Backend

## Phát Biểu Vấn Đề

**Chúng ta đang giải quyết vấn đề gì?**

Hiện tại dự án ZenSpa chưa có backend API để hỗ trợ các tính năng nghiệp vụ (quản lý lịch hẹn, khách hàng, nhân viên, dịch vụ...). Để phát triển hệ thống hoàn chỉnh, cần có nền tảng backend vững chắc với:

- Kết nối database PostgreSQL (Supabase) ổn định và an toàn
- Cấu trúc thư mục module rõ ràng, dễ mở rộng theo domain
- Cấu hình môi trường và quản lý credentials bảo mật
- Khả năng monitoring và health check cơ bản
- Cache layer (Redis) sẵn sàng cho optimization

**Ai bị ảnh hưởng bởi vấn đề này?**

- **Developers:** Không có nền tảng để phát triển các module nghiệp vụ
- **DevOps:** Không có endpoint để monitor trạng thái backend và database
- **Frontend Team:** Không có API để tích hợp các tính năng

**Tình hình hiện tại:**

- Chưa có backend API nào được triển khai
- Frontend đang tồn tại nhưng chưa có dữ liệu thật từ server
- Cần thiết lập cấu trúc chuẩn trước khi phát triển các module nghiệp vụ

## Mục Tiêu & Mục Đích

**Chúng ta muốn đạt được gì?**

### Mục tiêu chính

1. **Thiết lập FastAPI application** với cấu trúc module rõ ràng theo domain-driven design
2. **Kết nối database PostgreSQL** (Supabase) với connection pooling và error handling
3. **Tích hợp Redis** cho caching và session management
4. **Endpoint health check** để monitoring trạng thái hệ thống
5. **Environment configuration** an toàn và dễ quản lý

### Mục tiêu phụ

- Logging system rõ ràng để debug và monitoring (structured JSON logging)
- CORS middleware cho frontend integration
- Exception handlers chuẩn cho error response với error codes
- Documentation tự động với Swagger/OpenAPI
- Security baseline (headers, input validation, secrets management)
- Request tracking với Request ID
- API versioning strategy (prefix /api/v1/)

### Không mục tiêu (ngoài phạm vi)

- ❌ Supabase JWT authentication middleware (sẽ làm ở feature riêng)
- ❌ Business logic implementations (appointment, customer, staff modules)
- ❌ Socket.io real-time integration (sẽ làm sau)
- ❌ Rate limiting và advanced security features
- ⚠️ Alembic migrations setup (sẽ setup infrastructure nhưng chưa tạo migrations)

## Câu Chuyện Người Dùng & Trường Hợp Sử Dụng

**Người dùng sẽ tương tác với giải pháp như thế nào?**

### User Story 1: Database Connection

**Là một developer**, tôi muốn kết nối database PostgreSQL (Supabase) để có thể lưu trữ và truy xuất dữ liệu cho các module nghiệp vụ.

**Acceptance Criteria:**

- Connection string được quản lý qua environment variables
- Connection pooling được cấu hình phù hợp
- Database connection có retry mechanism và timeout
- Connection được kiểm tra khi startup và có health check endpoint

### User Story 2: Cấu Trúc Module

**Là một developer**, tôi cần cấu trúc thư mục module rõ ràng theo domain để dễ dàng phát triển và maintain các tính năng nghiệp vụ.

**Acceptance Criteria:**

- Thư mục `backend/app/modules/` sẵn sàng cho các domain
- Cấu trúc file chuẩn: `{domain}-models.py`, `{domain}-schemas.py`, `{domain}-service.py`, `{domain}-routes.py`
- Thư mục `core/` chứa config, database, security
- Thư mục `common/` chứa utilities và schemas dùng chung

### User Story 3: Health Check Endpoints

**Là một DevOps**, tôi cần endpoint `/health` để kiểm tra backend và database có hoạt động bình thường không.

**Acceptance Criteria:**

- `GET /health` - Trả về trạng thái tổng quan của hệ thống
- `GET /health/db` - Kiểm tra kết nối PostgreSQL
- `GET /health/redis` - Kiểm tra kết nối Redis
- Response format chuẩn với status code phù hợp (200/503)
- Response time dưới 1 giây

### User Story 4: Environment Configuration

**Là một developer**, tôi cần quản lý cấu hình môi trường (.env) rõ ràng để dễ dàng setup và bảo mật credentials.

**Acceptance Criteria:**

- File `.env.example` với tất cả variables cần thiết
- Pydantic Settings để validate và load env vars
- Hỗ trợ nhiều môi trường: development, staging, production
- Sensitive data không được commit vào git
- Documentation rõ ràng về cách setup env

### User Story 5: Redis Cache Setup

**Là một developer**, tôi cần Redis cache setup sẵn để các module sau có thể sử dụng cho caching và session management.

**Acceptance Criteria:**

- Redis connection được cấu hình qua environment
- Helper functions để get/set/delete cache
- Connection pool và error handling
- Health check endpoint cho Redis
- Documentation về cách sử dụng Redis helpers

### User Story 6: API Documentation

**Là một developer/tester**, tôi cần tài liệu API tự động để hiểu và test các endpoints.

**Acceptance Criteria:**

- Swagger UI tại `/docs`
- ReDoc tại `/redoc`
- OpenAPI schema đầy đủ
- Examples cho request/response

### User Story 7: Security Baseline

**Là một developer**, tôi cần security baseline được thiết lập từ đầu để đảm bảo ứng dụng an toàn và tuân thủ best practices.

**Acceptance Criteria:**

- Environment variables cho sensitive data (DATABASE_URL, Redis password, Supabase keys)
- File `.env.example` với template và comments giải thích
- `.gitignore` đảm bảo `.env` không được commit
- Security headers middleware (X-Content-Type-Options, X-Frame-Options, HSTS)
- Input validation với Pydantic cho tất cả request data
- Error messages không expose sensitive information (credentials, stack traces)
- CORS whitelist origins, không allow wildcard `*` trong production

### User Story 8: Error Handling Standards

**Là một frontend developer**, tôi cần error responses có format chuẩn và consistent để dễ dàng xử lý lỗi trong UI.

**Acceptance Criteria:**

- Error response format chuẩn: `{status: "error", error: {code, message, details}, timestamp, request_id}`
- Error codes được định nghĩa rõ ràng (VALIDATION_ERROR, DATABASE_ERROR, NOT_FOUND...)
- HTTP status codes mapping chính xác (400, 404, 422, 500, 503)
- Global exception handlers cho common exceptions
- Validation errors từ Pydantic được format đẹp
- Uncaught exceptions được catch và trả về generic error

### User Story 9: Request Tracking

**Là một DevOps**, tôi cần mỗi request có unique ID để trace logs và debug issues trong production.

**Acceptance Criteria:**

- Mỗi request được assign một unique Request ID (UUID)
- Request ID được log trong tất cả log messages liên quan
- Request ID được trả về trong response header `X-Request-ID`
- Request ID được include trong error responses
- Middleware tự động generate Request ID nếu client không gửi

### User Story 10: API Versioning

**Là một API developer**, tôi cần versioning strategy từ đầu để có thể phát triển API mà không breaking existing clients.

**Acceptance Criteria:**

- Tất cả API endpoints có prefix `/api/v1/`
- Health checks có thể ở global level `/health` hoặc versioned `/api/v1/health`
- API versioning strategy được document rõ ràng
- OpenAPI schema reflect correct version
- Cấu trúc code support multiple versions trong tương lai

## Tiêu Chí Thành Công

**Chúng ta sẽ biết khi nào hoàn thành?**

### Kết quả có thể đo lường

1. ✅ FastAPI app khởi động thành công trên port 8000
2. ✅ `/health`, `/health/db`, `/health/redis` đều trả về status 200
3. ✅ Database connection thành công với Supabase PostgreSQL
4. ✅ Redis connection thành công
5. ✅ Swagger docs hiển thị đầy đủ tại `/docs`
6. ✅ Logging xuất hiện trong console với format rõ ràng
7. ✅ CORS được cấu hình cho phép frontend connect

### Tiêu chí chấp nhận

- [ ] Tất cả health check endpoints hoạt động
- [ ] Environment variables được validate khi startup
- [ ] Error responses có format chuẩn với error codes
- [ ] Security headers được apply cho tất cả responses
- [ ] Request ID tracking hoạt động và được log
- [ ] API versioning với prefix `/api/v1/` implemented
- [ ] Code tuân thủ black và ruff formatting
- [ ] README.md có hướng dẫn setup chi tiết
- [ ] `.env.example` đầy đủ và có comment giải thích
- [ ] Alembic infrastructure được setup (config, folder structure)
- [ ] Structured JSON logging được configure

### Điểm chuẩn hiệu suất

- Health check response time < 1s (target: < 100ms)
- Database connection pool: min 5, max 20 connections
- Database connection timeout: 30s, retry 3 lần với exponential backoff
- Redis connection timeout: 5s, graceful fallback nếu unavailable
- API startup time < 3s
- Memory footprint < 200MB khi idle
- Middleware overhead < 10ms per request

## Ràng Buộc & Giả Định

**Chúng ta cần làm việc trong giới hạn nào?**

### Ràng buộc kỹ thuật

- **Backend framework:** FastAPI (bắt buộc)
- **Python version:** 3.12+
- **Database:** PostgreSQL 17+ trên Supabase (bắt buộc)
- **Cache:** Redis (bắt buộc)
- **ORM:** SQLModel với async support (sẽ dùng khi có models)

### Ràng buộc kinh doanh

- Phải tương thích với frontend Next.js đã có
- Phải chuẩn bị sẵn cho tích hợp Supabase Auth (nhưng chưa implement)
- Cấu trúc phải hỗ trợ nhiều domain module (appointment, customer, staff...)

### Ràng buộc thời gian

- Tính năng nền tảng này là prerequisite cho tất cả features khác
- Cần hoàn thành trước khi bắt đầu các module nghiệp vụ

### Giả định chúng ta đang đưa ra

1. Supabase project đã được tạo và có credentials
2. Redis server có sẵn (local hoặc cloud)
3. Developer đã cài Python 3.12+ và pip
4. Git đã được cấu hình
5. Frontend sẽ chạy trên `http://localhost:3000`

## Câu Hỏi & Vấn Đề Mở

**Chúng ta vẫn cần làm rõ gì?**

### Câu hỏi đã giải quyết

1. ✅ Redis sẽ dùng local development hay Redis Cloud?

   - **Quyết định:** Support cả hai - local (Docker) cho dev, Redis Cloud cho production
   - Configuration qua `REDIS_HOST` và `REDIS_PORT` trong `.env`

2. ✅ Có cần WebSocket support ngay từ đầu không?

   - **Quyết định:** Không, sẽ implement ở feature riêng

3. ✅ Logging level mặc định là gì?

   - **Quyết định:** INFO cho production, DEBUG cho development
   - Configurable qua `LOG_LEVEL` environment variable

4. ✅ Có cần request ID tracking không?

   - **Quyết định:** CÓ - thêm User Story 9 cho request tracking

5. ✅ Response format standards?

   - **Quyết định:** Success: `{status, data, message}`, Error: `{status, error: {code, message, details}, timestamp, request_id}`

6. ✅ Alembic setup có nằm trong scope không?
   - **Quyết định:** Setup infrastructure (folder, config) nhưng chưa tạo migrations cụ thể

### Câu hỏi chưa giải quyết

_(Không còn - tất cả đã được quyết định)_

### Vấn đề cần đầu vào từ bên liên quan

1. Xác nhận Supabase credentials (URL, anon key, service role key)
2. Xác định environment nào cần support (dev, staging, prod)
3. CORS origins cần allow (ngoài localhost:3000)

### Nghiên cứu cần thiết

1. Best practices cho FastAPI + Supabase integration
2. SQLModel async patterns với Supabase PostgreSQL
3. Redis connection pooling và graceful degradation
4. Structured logging với JSON format (python-json-logger hoặc structlog)
5. Request ID propagation patterns trong async context
6. Tenacity retry strategies cho database connections
7. Security headers best practices cho REST APIs
8. API versioning patterns (URL vs header vs content negotiation)
