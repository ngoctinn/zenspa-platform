---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
feature: backend-foundation
---

# Chiến Lược Kiểm Tra - Nền Tảng Backend

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- **Unit test coverage:** 100% cho code mới (core/, common/, redis/, api/)
- **Integration test coverage:** Tất cả health check endpoints và database/Redis connections
- **End-to-end test:** Basic API flow từ request → database/Redis → response
- **Manual testing:** Swagger UI, health endpoints, startup/shutdown lifecycle

### Căn Chỉnh Với Requirements

| Requirement            | Test Coverage                     |
| ---------------------- | --------------------------------- |
| Database connection    | ✅ Unit test + Integration test   |
| Redis connection       | ✅ Unit test + Integration test   |
| Health check endpoints | ✅ Integration test + Manual test |
| Environment config     | ✅ Unit test                      |
| CORS middleware        | ✅ Integration test               |
| Exception handlers     | ✅ Unit test                      |
| Logging setup          | ✅ Unit test                      |

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### Configuration Management (`test_config.py`)

- [x] **Test 1.1:** Load environment variables thành công

  - Scenario: `.env` file với tất cả required vars
  - Expected: Settings object được tạo với correct values
  - Coverage: Config loading, validation

- [x] **Test 1.2:** Validate required fields

  - Scenario: Missing `DATABASE_URL`
  - Expected: Validation error được raise
  - Coverage: Pydantic validation

- [x] **Test 1.3:** Parse CORS origins từ string sang list

  - Scenario: `CORS_ORIGINS="http://localhost:3000,http://localhost:8080"`
  - Expected: `settings.cors_origins_list` = `["http://localhost:3000", "http://localhost:8080"]`
  - Coverage: Property method

- [x] **Test 1.4:** Default values hoạt động
  - Scenario: Optional env vars không set
  - Expected: Default values được sử dụng
  - Coverage: Default value logic

### Database Layer (`test_database.py`)

- [x] **Test 2.1:** Create async engine thành công

  - Scenario: Valid `DATABASE_URL`
  - Expected: Engine được tạo với correct config
  - Coverage: Engine initialization

- [x] **Test 2.2:** Session factory tạo async session

  - Scenario: Call `get_async_session()`
  - Expected: AsyncSession object được yield
  - Coverage: Session management

- [x] **Test 2.3:** Health check với database healthy

  - Scenario: Database available
  - Expected: `(True, response_time > 0)`
  - Coverage: Health check success path

- [x] **Test 2.4:** Health check với database down

  - Scenario: Database unavailable
  - Expected: `(False, 0.0)`
  - Coverage: Health check error handling

- [x] **Test 2.5:** Init DB connection

  - Scenario: Call `init_db()`
  - Expected: Connection established, no errors
  - Coverage: Startup logic

- [x] **Test 2.6:** Close DB connection
  - Scenario: Call `close_db()`
  - Expected: Engine disposed, connections closed
  - Coverage: Shutdown logic

### Redis Layer (`test_redis.py`)

- [x] **Test 3.1:** Redis connection initialization

  - Scenario: Valid Redis config
  - Expected: Redis client connected
  - Coverage: Redis init

- [x] **Test 3.2:** Redis health check when healthy

  - Scenario: Redis available
  - Expected: `(True, response_time > 0)`
  - Coverage: Health check success

- [x] **Test 3.3:** Redis health check when down

  - Scenario: Redis unavailable
  - Expected: `(False, 0.0)`
  - Coverage: Graceful degradation

- [x] **Test 3.4:** Cache get/set/delete operations

  - Scenario: `cache_set("key", "value", 60)`, `cache_get("key")`, `cache_delete("key")`
  - Expected: All operations succeed, value retrieved correctly
  - Coverage: Cache helpers

- [x] **Test 3.5:** Cache TTL expiration
  - Scenario: Set cache với TTL = 1 second, wait 2 seconds, get
  - Expected: Value expired, returns None
  - Coverage: TTL behavior

### Exception Handling (`test_exceptions.py`)

- [x] **Test 4.1:** ZenSpaException custom exception

  - Scenario: Raise `ZenSpaException("error", "CODE")`
  - Expected: Exception với correct message và code
  - Coverage: Custom exception class

- [x] **Test 4.2:** ZenSpa exception handler

  - Scenario: Endpoint raises `ZenSpaException`
  - Expected: JSON response với standard error format
  - Coverage: Exception handler

- [x] **Test 4.3:** Validation exception handler

  - Scenario: Invalid request body
  - Expected: 422 response với validation details
  - Coverage: Pydantic validation errors

- [x] **Test 4.4:** General exception handler
  - Scenario: Uncaught exception
  - Expected: 500 response với generic error message
  - Coverage: Fallback error handling

### Logging (`test_logging.py`)

- [x] **Test 5.1:** Logging setup với correct level

  - Scenario: `LOG_LEVEL=INFO`
  - Expected: Logger configured với INFO level
  - Coverage: Logging configuration

- [x] **Test 5.2:** Log messages được output
  - Scenario: Log INFO message
  - Expected: Message appears in stdout với correct format
  - Coverage: Log output

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

### Health Check Endpoints (`test_health_integration.py`)

- [x] **Integration 1.1:** `GET /health` endpoint

  - Setup: App running
  - Request: `GET /health`
  - Expected: 200 OK, JSON với status="healthy", service name, version
  - Validates: Basic health check, FastAPI routing

- [x] **Integration 1.2:** `GET /health/db` với database healthy

  - Setup: Database connected
  - Request: `GET /health/db`
  - Expected: 200 OK, `connected=true`, `response_time_ms > 0`
  - Validates: Database health check, database connection

- [x] **Integration 1.3:** `GET /health/db` với database down

  - Setup: Mock database unavailable
  - Request: `GET /health/db`
  - Expected: 503 Service Unavailable, `connected=false`
  - Validates: Error handling, status codes

- [x] **Integration 1.4:** `GET /health/redis` với Redis healthy

  - Setup: Redis connected
  - Request: `GET /health/redis`
  - Expected: 200 OK, `connected=true`, `response_time_ms > 0`
  - Validates: Redis health check, Redis connection

- [x] **Integration 1.5:** `GET /health/redis` với Redis down
  - Setup: Redis unavailable
  - Request: `GET /health/redis`
  - Expected: 503 Service Unavailable, `connected=false`
  - Validates: Graceful degradation

### CORS Configuration (`test_cors_integration.py`)

- [x] **Integration 2.1:** CORS headers với allowed origin

  - Setup: `CORS_ORIGINS=http://localhost:3000`
  - Request: `OPTIONS /health` với `Origin: http://localhost:3000`
  - Expected: Response có `Access-Control-Allow-Origin: http://localhost:3000`
  - Validates: CORS middleware

- [x] **Integration 2.2:** CORS reject với disallowed origin
  - Setup: `CORS_ORIGINS=http://localhost:3000`
  - Request: `OPTIONS /health` với `Origin: http://evil.com`
  - Expected: No CORS headers
  - Validates: CORS security

### Application Lifecycle (`test_lifecycle_integration.py`)

- [x] **Integration 3.1:** Startup event initializes connections

  - Action: Start app
  - Expected: Database và Redis connections initialized
  - Validates: Lifespan startup

- [x] **Integration 3.2:** Shutdown event closes connections
  - Action: Stop app
  - Expected: All connections closed gracefully
  - Validates: Lifespan shutdown

### API Documentation (`test_docs_integration.py`)

- [x] **Integration 4.1:** Swagger UI accessible

  - Request: `GET /docs`
  - Expected: 200 OK, HTML page
  - Validates: Swagger UI serving

- [x] **Integration 4.2:** OpenAPI schema valid
  - Request: `GET /openapi.json`
  - Expected: 200 OK, valid OpenAPI 3.0 JSON
  - Validates: API schema generation

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

### E2E 1: Complete Health Check Flow

- [x] **Scenario:** DevOps kiểm tra health của toàn bộ system
  - **Steps:**
    1. Start backend application
    2. Request `GET /health` → Verify 200 OK
    3. Request `GET /health/db` → Verify database connected
    4. Request `GET /health/redis` → Verify Redis connected
  - **Expected:** Tất cả health checks pass, response time < 1s
  - **Validates:** Complete monitoring flow

### E2E 2: Application Startup to First Request

- [x] **Scenario:** Developer start app và test first endpoint
  - **Steps:**
    1. `uvicorn app.main:app --reload`
    2. Wait for startup logs
    3. Request `GET /` (root endpoint)
    4. Verify API docs at `/docs`
  - **Expected:** App starts < 3s, endpoints accessible
  - **Validates:** Development workflow

### E2E 3: Error Handling Flow

- [x] **Scenario:** Client gửi invalid request
  - **Steps:**
    1. Request endpoint with invalid data
    2. Verify error response format
    3. Check logs for error tracking
  - **Expected:** Standard error response, không expose internals
  - **Validates:** Error handling UX

## Dữ Liệu Kiểm Tra

**Chúng ta sử dụng dữ liệu nào để kiểm tra?**

### Environment Variables Test Data

```python
# .env.test
APP_NAME=ZenSpa Backend Test
APP_VERSION=0.1.0
DEBUG=True
ENVIRONMENT=testing
DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/zenspa_test
REDIS_HOST=localhost
REDIS_PORT=6379
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=DEBUG
```

### Mock Data

```python
# Mock Redis responses
mock_redis_ping = asyncio.Future()
mock_redis_ping.set_result(True)

# Mock database query results
mock_db_result = [(1,)]  # SELECT 1 result
```

### Test Fixtures (`conftest.py`)

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_settings():
    """Mock settings object"""
    return Settings(
        DATABASE_URL="postgresql+asyncpg://test:test@localhost/test",
        REDIS_HOST="localhost",
        REDIS_PORT=6379,
    )
```

## Báo Cáo & Bao Phủ Kiểm Tra

**Chúng ta xác minh và giao tiếp kết quả kiểm tra như thế nào?**

### Coverage Commands

```bash
# Run tests với coverage
pytest --cov=app --cov-report=html --cov-report=term

# Coverage target: 80%+
# Threshold settings trong pytest.ini
[pytest]
addopts = --cov=app --cov-fail-under=80
```

### Expected Coverage Report

```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
app/__init__.py                       0      0   100%
app/main.py                          45      2    96%
app/core/config.py                   25      0   100%
app/core/database.py                 40      3    93%
app/core/exceptions.py               30      0   100%
app/core/logging.py                  15      0   100%
app/redis/client.py                  35      3    91%
app/redis/helpers.py                 20      1    95%
app/common/schemas.py                15      0   100%
app/api/health.py                    30      0   100%
app/api/api_v1.py                     5      0   100%
-----------------------------------------------------
TOTAL                               260     9    97%
```

### Coverage Gaps

| File              | Coverage | Gap                        | Reason                   |
| ----------------- | -------- | -------------------------- | ------------------------ |
| `main.py`         | 96%      | Shutdown event edge case   | Hard to test, low risk   |
| `database.py`     | 93%      | Connection retry logic     | Requires complex mocking |
| `redis/client.py` | 91%      | Connection pool edge cases | Low priority             |

### Test Report Links

- **Coverage HTML:** `htmlcov/index.html`
- **Pytest report:** Console output
- **CI/CD:** GitHub Actions test results (future)

## Kiểm Tra Thủ Công

**Điều gì cần xác thực của con người?**

### Checklist Kiểm Tra Manual

#### 1. API Documentation

- [x] Navigate to `http://localhost:8000/docs`
- [x] Verify all endpoints hiển thị đúng
- [x] Test "Try it out" cho mỗi endpoint
- [x] Verify response schemas correct
- [x] Check OpenAPI schema tại `/openapi.json`

#### 2. Health Check Endpoints

- [x] Test `GET /health` từ browser/Postman
- [x] Test `GET /health/db` → Verify database info
- [x] Test `GET /health/redis` → Verify Redis info
- [x] Verify response times < 1s
- [x] Check status codes (200 vs 503)

#### 3. Application Lifecycle

- [x] Start app: `uvicorn app.main:app --reload`
- [x] Verify startup logs hiển thị:
  - ✅ Database connected
  - ✅ Redis connected
  - ✅ App started successfully
- [x] Stop app (Ctrl+C)
- [x] Verify shutdown logs:
  - ✅ Database connections closed
  - ✅ Redis connection closed
  - ✅ App stopped

#### 4. Error Handling

- [x] Test invalid endpoint: `GET /invalid`
- [x] Verify 404 error response format
- [x] Test với database down
- [x] Verify graceful error messages

#### 5. CORS Configuration

- [x] Test từ frontend `http://localhost:3000`
- [x] Verify no CORS errors trong browser console
- [x] Test từ disallowed origin
- [x] Verify CORS blocked

#### 6. Environment Configuration

- [x] Test với `.env` file
- [x] Test với environment variables
- [x] Test missing required vars → Verify error
- [x] Test invalid values → Verify validation error

### Browser Compatibility

- ✅ Chrome (API docs, fetch requests)
- ✅ Firefox (API docs, fetch requests)
- ⚠️ Safari (không cần test - backend API)

### Device Testing

- ⚠️ Không áp dụng (backend API, không có UI)

## Kiểm Tra Hiệu Suất

**Chúng ta xác thực hiệu suất như thế nào?**

### Performance Benchmarks

| Metric                   | Target  | Measurement Method                    |
| ------------------------ | ------- | ------------------------------------- |
| Startup time             | < 3s    | Time từ `uvicorn` start đến app ready |
| `/health` response       | < 100ms | Average over 100 requests             |
| `/health/db` response    | < 500ms | Average over 100 requests             |
| `/health/redis` response | < 50ms  | Average over 100 requests             |
| Memory footprint         | < 200MB | `ps aux` khi idle                     |

### Load Testing Scenarios

```bash
# Sử dụng Apache Bench (ab)

# Test 1: Basic load test
ab -n 1000 -c 10 http://localhost:8000/health

# Test 2: Database health check load
ab -n 500 -c 5 http://localhost:8000/health/db

# Test 3: Redis health check load
ab -n 1000 -c 10 http://localhost:8000/health/redis
```

### Expected Performance Results

```
# GET /health
Requests per second:    1000+ [#/sec]
Time per request:       1-5 ms [mean]
Failed requests:        0

# GET /health/db
Requests per second:    200+ [#/sec]
Time per request:       10-50 ms [mean]
Failed requests:        0

# GET /health/redis
Requests per second:    500+ [#/sec]
Time per request:       2-10 ms [mean]
Failed requests:        0
```

### Stress Testing

```bash
# Concurrent connections stress test
ab -n 10000 -c 100 http://localhost:8000/health

# Expected: No 500 errors, response time degrades gracefully
```

## Theo Dõi Lỗi

**Chúng ta quản lý vấn đề như thế nào?**

### Issue Tracking Process

1. **Bug Discovery:** Trong testing phase
2. **Log Issue:** Create GitHub issue với:
   - Title: `[Bug] Brief description`
   - Labels: `bug`, `backend-foundation`
   - Description: Steps to reproduce, expected vs actual
3. **Severity Assignment:**
   - 🔴 Critical: App không start, data loss
   - 🟡 Major: Feature không hoạt động
   - 🟢 Minor: Edge case, cosmetic
4. **Fix & Retest:** Fix bug, add regression test
5. **Close Issue:** Verify fix trong integration test

### Bug Severity Levels

| Level    | Description                    | SLA              |
| -------- | ------------------------------ | ---------------- |
| Critical | App crash, security issue      | Fix immediately  |
| Major    | Feature broken, wrong behavior | Fix before merge |
| Minor    | Edge case, non-critical        | Fix or defer     |
| Trivial  | Cosmetic, typo                 | Nice to fix      |

### Regression Testing Strategy

- **After bug fix:** Add test case covering the bug
- **Before release:** Run full test suite
- **Continuous:** Run tests on every commit (CI/CD)

### Test Failure Handling

```bash
# Khi test fail:
1. Read error message carefully
2. Check logs for details
3. Debug với pytest -vv -s (verbose + print)
4. Fix code or update test
5. Re-run: pytest tests/test_file.py::test_name
6. Verify all tests pass
```

## Test Execution Plan

### Phase 1: Unit Tests (Day 1, 30 min)

```bash
# Run all unit tests
pytest tests/test_config.py -v
pytest tests/test_database.py -v
pytest tests/test_redis.py -v
pytest tests/test_exceptions.py -v
pytest tests/test_logging.py -v

# Expected: All pass, coverage > 90%
```

### Phase 2: Integration Tests (Day 1, 20 min)

```bash
# Run integration tests
pytest tests/test_health_integration.py -v
pytest tests/test_cors_integration.py -v
pytest tests/test_lifecycle_integration.py -v
pytest tests/test_docs_integration.py -v

# Expected: All pass, endpoints work correctly
```

### Phase 3: E2E Tests (Day 1, 15 min)

```bash
# Manual E2E testing
# Follow manual checklist above

# Expected: All scenarios work end-to-end
```

### Phase 4: Performance Tests (Day 1, 15 min)

```bash
# Run load tests
ab -n 1000 -c 10 http://localhost:8000/health
ab -n 500 -c 5 http://localhost:8000/health/db
ab -n 1000 -c 10 http://localhost:8000/health/redis

# Expected: Meet performance benchmarks
```

## Test Success Criteria

✅ **All tests pass:**

- Unit tests: 100% pass
- Integration tests: 100% pass
- E2E tests: All scenarios work

✅ **Coverage goals met:**

- Overall coverage > 80%
- Core modules coverage = 100%

✅ **Performance benchmarks met:**

- All endpoints < target response time
- No memory leaks
- Handles concurrent requests

✅ **Manual verification complete:**

- All checklist items verified
- Documentation accurate
- Error messages user-friendly

✅ **Ready for production:**

- No critical bugs
- All features working as designed
- Code review approved
