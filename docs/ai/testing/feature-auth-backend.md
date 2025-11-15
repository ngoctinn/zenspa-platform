---
phase: testing
title: Chiến Lược Kiểm Tra - Auth Backend Module
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
feature: auth-backend
---

# Chiến Lược Kiểm Tra - Auth Backend Module

## Mục Tiêu Bao Phủ Kiểm Tra

**Mục tiêu:**

- **Unit tests:** 100% coverage cho tất cả functions trong auth module
- **Integration tests:** Tất cả API endpoints và database interactions
- **E2E tests:** Complete auth flows từ webhook → login → protected endpoints
- **Security tests:** JWT verification, role checks, webhook signature validation

**Alignment với yêu cầu:**

- [US-1] JWT verification được test với valid/invalid/expired tokens
- [US-2] Role-based authorization test cho tất cả role combinations
- [US-3] GET /auth/me endpoint test với caching
- [US-4] Auto-assign customer role test via webhook
- [US-5] Audit log creation test cho tất cả events
- [US-6] Multi-role support test

## Kiểm Tra Đơn Vị

### Component 1: JWT Verification (`app/core/auth.py`)

#### Test 1.1: Valid JWT Token

**Mô tả:** Verify JWT token hợp lệ thành công

**Setup:**

```python
import pytest
from unittest.mock import patch, MagicMock
from app.core.auth import verify_jwt_token

@pytest.fixture
def valid_jwt_payload():
    return {
        "sub": "user-uuid-123",
        "email": "test@example.com",
        "exp": 9999999999  # Far future
    }

@pytest.fixture
def mock_public_key():
    return "mock-rsa-public-key"
```

**Test cases:**

- [ ] Test 1.1.1: Decode valid token với correct signature → return payload
- [ ] Test 1.1.2: Extract user_id và email từ payload correctly
- [ ] Test 1.1.3: Cache public key after first fetch

```python
@patch("app.core.auth.get_supabase_public_key")
@patch("jwt.decode")
def test_verify_valid_token(mock_decode, mock_get_key, valid_jwt_payload):
    mock_get_key.return_value = "public-key"
    mock_decode.return_value = valid_jwt_payload

    result = verify_jwt_token("valid.jwt.token")

    assert result["sub"] == "user-uuid-123"
    assert result["email"] == "test@example.com"
    mock_decode.assert_called_once()
```

#### Test 1.2: Invalid/Expired JWT Tokens

**Mô tả:** Reject invalid hoặc expired tokens

**Test cases:**

- [ ] Test 1.2.1: Expired token → raise HTTPException 401 "Token đã hết hạn"
- [ ] Test 1.2.2: Invalid signature → raise HTTPException 401 "Token không hợp lệ"
- [ ] Test 1.2.3: Malformed token → raise HTTPException 401
- [ ] Test 1.2.4: Missing token → raise HTTPException 401

```python
import jwt
from fastapi import HTTPException

@patch("jwt.decode")
def test_verify_expired_token(mock_decode):
    mock_decode.side_effect = jwt.ExpiredSignatureError()

    with pytest.raises(HTTPException) as exc_info:
        verify_jwt_token("expired.jwt.token")

    assert exc_info.value.status_code == 401
    assert "hết hạn" in exc_info.value.detail["message"]
```

#### Test 1.3: Extract Token from Header

**Test cases:**

- [ ] Test 1.3.1: Valid "Bearer <token>" → extract token
- [ ] Test 1.3.2: Missing "Bearer" prefix → raise 401
- [ ] Test 1.3.3: Empty Authorization header → raise 401
- [ ] Test 1.3.4: None Authorization header → raise 401

---

### Component 2: CurrentUser Dependency (`app/core/auth.py`)

#### Test 2.1: Load User with Roles

**Mô tả:** Load authenticated user với roles từ database

**Setup:**

```python
@pytest.fixture
def db_session():
    # Setup in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_user_roles(db_session):
    user_id = uuid.uuid4()
    roles = [
        UserRole(user_id=user_id, role="customer"),
        UserRole(user_id=user_id, role="staff")
    ]
    for role in roles:
        db_session.add(role)
    db_session.commit()
    return user_id
```

**Test cases:**

- [ ] Test 2.1.1: User với 1 role → CurrentUser.roles = ["customer"]
- [ ] Test 2.1.2: User với multi-roles → CurrentUser.roles = ["customer", "staff"]
- [ ] Test 2.1.3: User không có roles → CurrentUser.roles = []
- [ ] Test 2.1.4: Load profile nếu tồn tại → CurrentUser.profile = Profile(...)

#### Test 2.2: CurrentUser Helper Methods

**Test cases:**

- [ ] Test 2.2.1: has_role("customer") → True khi user có role customer
- [ ] Test 2.2.2: has_role("admin") → False khi user không có role admin
- [ ] Test 2.2.3: has_any_role(["staff", "admin"]) → True với multi-role check
- [ ] Test 2.2.4: is_customer(), is_staff(), is_admin() shortcuts work correctly

```python
def test_current_user_has_role():
    user = CurrentUser(
        user_id=uuid.uuid4(),
        email="test@example.com",
        roles=["customer", "staff"]
    )

    assert user.has_role("customer") is True
    assert user.has_role("staff") is True
    assert user.has_role("admin") is False
    assert user.has_any_role(["admin", "staff"]) is True
```

---

### Component 3: Role-Based Dependencies (`app/core/auth.py`)

#### Test 3.1: require_role Dependency

**Test cases:**

- [ ] Test 3.1.1: User có required role → allow access
- [ ] Test 3.1.2: User không có required role → raise HTTPException 403
- [ ] Test 3.1.3: Error message chứa role name

```python
@pytest.mark.asyncio
async def test_require_role_success():
    user = CurrentUser(user_id=uuid.uuid4(), email="test@example.com", roles=["staff"])
    dependency = require_role("staff")

    result = await dependency(current_user=user)

    assert result == user

@pytest.mark.asyncio
async def test_require_role_forbidden():
    user = CurrentUser(user_id=uuid.uuid4(), email="test@example.com", roles=["customer"])
    dependency = require_role("admin")

    with pytest.raises(HTTPException) as exc_info:
        await dependency(current_user=user)

    assert exc_info.value.status_code == 403
```

#### Test 3.2: require_roles Multi-Role Check

**Test cases:**

- [ ] Test 3.2.1: User có ít nhất 1 role trong list → allow
- [ ] Test 3.2.2: User không có role nào trong list → raise 403
- [ ] Test 3.2.3: Empty roles list → raise 403

---

### Component 4: Auth Service (`app/modules/auth/auth-service.py`)

#### Test 4.1: assign_role Function

**Test cases:**

- [ ] Test 4.1.1: Assign new role → create UserRole record
- [ ] Test 4.1.2: Assign existing role → idempotent (không duplicate)
- [ ] Test 4.1.3: Audit log created với event_type="role.assigned"
- [ ] Test 4.1.4: Cache invalidated after role assignment

```python
def test_assign_role_creates_record(db_session):
    user_id = uuid.uuid4()
    admin_id = uuid.uuid4()

    assign_role(
        user_id=user_id,
        role="staff",
        assigned_by=admin_id,
        session=db_session,
        ip="127.0.0.1"
    )

    # Verify UserRole created
    role_record = db_session.exec(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role == "staff"
        )
    ).first()

    assert role_record is not None
    assert role_record.assigned_by == admin_id
```

#### Test 4.2: revoke_role Function

**Test cases:**

- [ ] Test 4.2.1: Revoke existing role → delete UserRole record
- [ ] Test 4.2.2: Revoke non-existing role → no error (idempotent)
- [ ] Test 4.2.3: Audit log created với event_type="role.revoked"
- [ ] Test 4.2.4: Cache invalidated after revoke

#### Test 4.3: log_audit_event Function

**Test cases:**

- [ ] Test 4.3.1: Create audit log với all fields → AuditLog record created
- [ ] Test 4.3.2: JSONB metadata stored correctly
- [ ] Test 4.3.3: IP address và user_agent captured

---

### Component 5: Models Validation (`app/modules/auth/auth-models.py`)

#### Test 5.1: UserRole Model

**Test cases:**

- [ ] Test 5.1.1: Valid role ("customer", "staff", "admin") → accept
- [ ] Test 5.1.2: Invalid role → raise validation error (check constraint)
- [ ] Test 5.1.3: Duplicate (user_id, role) → raise unique constraint error
- [ ] Test 5.1.4: Foreign key cascade delete → UserRole deleted when user deleted

#### Test 5.2: Profile Model

**Test cases:**

- [ ] Test 5.2.1: Unique user_id constraint enforced
- [ ] Test 5.2.2: Nullable fields (full_name, avatar_url) work correctly
- [ ] Test 5.2.3: Timestamps auto-populate (created_at, updated_at)

---

## Kiểm Tra Tích Hợp

### Scenario 1: GET /api/v1/auth/me Endpoint

**Setup:**

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Generate valid JWT token for testing
    token = create_test_jwt_token(user_id="test-uuid", email="test@example.com")
    return {"Authorization": f"Bearer {token}"}
```

**Test cases:**

- [ ] Test I1.1: Authenticated request → 200 OK với user info

  ```python
  def test_get_me_authenticated(auth_headers, db_session):
      response = client.get("/api/v1/auth/me", headers=auth_headers)

      assert response.status_code == 200
      data = response.json()
      assert "user_id" in data
      assert "email" in data
      assert "roles" in data
  ```

- [ ] Test I1.2: Missing Authorization header → 401 Unauthorized
- [ ] Test I1.3: Invalid JWT token → 401 Unauthorized
- [ ] Test I1.4: Expired JWT token → 401 Unauthorized
- [ ] Test I1.5: Response includes profile data nếu tồn tại
- [ ] Test I1.6: Response includes all roles (multi-role)

---

### Scenario 2: POST /api/v1/auth/roles (Assign Role)

**Test cases:**

- [ ] Test I2.1: Admin assign role to user → 201 Created

  ```python
  def test_assign_role_as_admin(admin_auth_headers, db_session):
      payload = {
          "user_id": str(uuid.uuid4()),
          "role": "staff"
      }
      response = client.post(
          "/api/v1/auth/roles",
          json=payload,
          headers=admin_auth_headers
      )

      assert response.status_code == 201
      assert response.json()["role"] == "staff"
  ```

- [ ] Test I2.2: Non-admin user → 403 Forbidden
- [ ] Test I2.3: Invalid role value → 422 Validation error
- [ ] Test I2.4: Assign existing role → idempotent (200 OK)
- [ ] Test I2.5: Audit log created after assignment

---

### Scenario 3: DELETE /api/v1/auth/roles/{user_id}/{role}

**Test cases:**

- [ ] Test I3.1: Admin revoke role → 200 OK
- [ ] Test I3.2: Non-admin user → 403 Forbidden
- [ ] Test I3.3: Revoke non-existing role → 200 OK (idempotent)
- [ ] Test I3.4: Audit log created after revocation
- [ ] Test I3.5: User immediately loses access to role-protected endpoints

---

### Scenario 4: Webhook Handler POST /api/v1/webhooks/auth/user-created

**Test cases:**

- [ ] Test I4.1: Valid webhook signature + new user → 200 OK, profile + role created

  ```python
  def test_webhook_user_created(db_session):
      payload = {
          "type": "INSERT",
          "table": "users",
          "record": {
              "id": str(uuid.uuid4()),
              "email": "newuser@example.com"
          }
      }
      signature = generate_webhook_signature(payload)

      response = client.post(
          "/api/v1/webhooks/auth/user-created",
          json=payload,
          headers={"X-Supabase-Signature": signature}
      )

      assert response.status_code == 200
      # Verify Profile created
      # Verify UserRole created with role="customer"
  ```

- [ ] Test I4.2: Invalid signature → 401 Unauthorized
- [ ] Test I4.3: Duplicate user (idempotent) → 200 OK, no duplicate records
- [ ] Test I4.4: Audit log created với event_type="user.created"

---

## Kiểm Tra End-to-End

### E2E Flow 1: New User Registration → Login → Access Protected Endpoint

**Steps:**

1. Webhook triggered (user created in Supabase)
2. Backend creates profile + assigns customer role
3. User logs in (frontend gets JWT)
4. User calls GET /auth/me → success
5. User calls customer-only endpoint → success
6. User calls staff-only endpoint → 403 Forbidden

**Test:**

```python
def test_e2e_new_user_flow():
    # Step 1: Simulate webhook
    user_id = str(uuid.uuid4())
    webhook_payload = {
        "record": {"id": user_id, "email": "newuser@example.com"}
    }
    webhook_response = client.post("/webhooks/auth/user-created", json=webhook_payload, ...)
    assert webhook_response.status_code == 200

    # Step 2: Generate JWT for user
    token = create_test_jwt_token(user_id=user_id, email="newuser@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: GET /auth/me
    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert "customer" in me_response.json()["roles"]

    # Step 4: Access customer endpoint → success
    customer_response = client.get("/api/v1/customer/profile", headers=headers)
    assert customer_response.status_code == 200

    # Step 5: Access staff endpoint → forbidden
    staff_response = client.get("/api/v1/staff/dashboard", headers=headers)
    assert staff_response.status_code == 403
```

---

### E2E Flow 2: Admin Assigns Staff Role → User Gains Access

**Steps:**

1. User initially has only customer role
2. Admin assigns staff role
3. User accesses staff endpoint → success (after cache TTL or invalidation)

**Test:**

- [ ] Verify role assignment propagates correctly
- [ ] Verify cache invalidation works
- [ ] Verify audit log tracks role change

---

### E2E Flow 3: Audit Log Query

**Steps:**

1. Perform multiple actions (login, assign role, revoke role)
2. Admin queries audit logs
3. Verify all events logged correctly

**Test:**

- [ ] GET /api/v1/auth/audit-logs?user_id=X → returns all events for user
- [ ] Filter by event_type works
- [ ] Pagination works correctly

---

## Dữ Liệu Kiểm Tra

### Test Fixtures

**JWT Tokens:**

```python
import jwt
from datetime import datetime, timedelta

def create_test_jwt_token(user_id: str, email: str, roles: list[str] = None) -> str:
    """Generate valid JWT for testing."""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, "test-secret", algorithm="HS256")

def create_expired_jwt_token() -> str:
    """Generate expired JWT for testing."""
    payload = {
        "sub": "test-user",
        "email": "test@example.com",
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    return jwt.encode(payload, "test-secret", algorithm="HS256")
```

**Database Seed Data:**

```python
@pytest.fixture
def seed_test_users(db_session):
    """Create test users với different roles."""
    users = [
        {
            "user_id": uuid.uuid4(),
            "email": "customer@example.com",
            "roles": ["customer"]
        },
        {
            "user_id": uuid.uuid4(),
            "email": "staff@example.com",
            "roles": ["staff"]
        },
        {
            "user_id": uuid.uuid4(),
            "email": "admin@example.com",
            "roles": ["admin"]
        },
        {
            "user_id": uuid.uuid4(),
            "email": "multi@example.com",
            "roles": ["customer", "staff"]
        }
    ]

    for user_data in users:
        profile = Profile(user_id=user_data["user_id"], full_name="Test User")
        db_session.add(profile)

        for role in user_data["roles"]:
            user_role = UserRole(user_id=user_data["user_id"], role=role)
            db_session.add(user_role)

    db_session.commit()
    return users
```

---

## Báo Cáo & Bao Phủ Kiểm Tra

### Commands

**Run all tests:**

```bash
pytest tests/test_auth/
```

**Run with coverage:**

```bash
pytest --cov=app/modules/auth --cov=app/core/auth --cov-report=html --cov-report=term
```

**Coverage thresholds:**

```ini
# pytest.ini or pyproject.toml
[tool:pytest]
addopts = --cov-fail-under=100
```

### Expected Coverage

**Target: 100% coverage cho auth module**

| File                             | Lines   | Coverage | Missing |
| -------------------------------- | ------- | -------- | ------- |
| app/core/auth.py                 | 150     | 100%     | -       |
| app/modules/auth/auth-models.py  | 50      | 100%     | -       |
| app/modules/auth/auth-schemas.py | 30      | 100%     | -       |
| app/modules/auth/auth-service.py | 80      | 100%     | -       |
| app/modules/auth/auth-routes.py  | 60      | 100%     | -       |
| app/modules/auth/webhook.py      | 40      | 100%     | -       |
| **TOTAL**                        | **410** | **100%** | **-**   |

**Khoảng trống bao phủ (nếu có):**

- Error handling paths cần test đầy đủ
- Edge cases: empty roles, null profiles, etc.
- Race conditions trong cache invalidation (nếu có)

---

## Kiểm Tra Thủ Công

### Checklist UI/UX (Frontend integration later)

- [ ] Login flow works end-to-end
- [ ] Protected pages redirect to login nếu chưa authenticated
- [ ] Role-based UI rendering correct (customer vs staff vs admin)
- [ ] Token refresh works seamlessly
- [ ] Logout clears auth state

### API Testing (Postman/Insomnia)

**Collection:**

```json
{
  "name": "Auth Backend Tests",
  "requests": [
    {
      "name": "GET /auth/me",
      "method": "GET",
      "url": "{{base_url}}/api/v1/auth/me",
      "headers": {
        "Authorization": "Bearer {{jwt_token}}"
      },
      "tests": ["Status code is 200", "Response contains user_id, email, roles"]
    },
    {
      "name": "POST /auth/roles (Admin)",
      "method": "POST",
      "url": "{{base_url}}/api/v1/auth/roles",
      "headers": {
        "Authorization": "Bearer {{admin_jwt_token}}"
      },
      "body": {
        "user_id": "{{test_user_id}}",
        "role": "staff"
      },
      "tests": ["Status code is 201", "Audit log created"]
    }
  ]
}
```

### Browser/Device Compatibility

- [ ] Chrome/Firefox/Safari (latest versions)
- [ ] Mobile browsers (iOS Safari, Chrome Android)
- [ ] CORS headers correct
- [ ] HTTPS enforced in production

---

## Kiểm Tra Hiệu Suất

### Load Testing (Locust/k6)

**Scenario: JWT Verification Performance**

```python
from locust import HttpUser, task, between

class AuthUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_me(self):
        self.client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {self.jwt_token}"}
        )
```

**Metrics:**

- [ ] P50 latency < 50ms
- [ ] P95 latency < 100ms
- [ ] P99 latency < 200ms
- [ ] Throughput: 1000 req/s với 10,000 concurrent users

### Cache Performance

**Test scenarios:**

- [ ] Cache hit rate > 90% cho user roles
- [ ] Cache miss → DB query < 50ms
- [ ] Redis down → graceful fallback, latency < 150ms

---

## Theo Dõi Lỗi

### Issue Tracking

**Bug template:**

```markdown
## Bug: [Short description]

**Severity:** Critical / Major / Minor

**Steps to Reproduce:**

1. Step 1
2. Step 2
3. ...

**Expected:** [What should happen]
**Actual:** [What actually happened]

**Environment:**

- Python version:
- FastAPI version:
- Supabase project:

**Logs:**
```

[Paste relevant logs]

```

**Related tests:**
- [ ] Unit test: test_xyz
- [ ] Integration test: test_abc
```

### Regression Testing

**Tự động chạy sau mỗi bug fix:**

```bash
pytest tests/test_auth/ -v --tb=short
```

**Checklist:**

- [ ] Bug fix implemented
- [ ] Regression test added
- [ ] All existing tests pass
- [ ] Coverage maintained at 100%
