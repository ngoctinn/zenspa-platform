---
phase: implementation
title: Hướng Dẫn Triển Khai - Auth Backend Module
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
feature: auth-backend
---

# Hướng Dẫn Triển Khai - Auth Backend Module

## Thiết Lập Phát Triển

**Điều kiện tiên quyết:**

- Python 3.12+
- PostgreSQL 17+ (Supabase)
- Redis 7+
- Git

**Cài đặt dependencies:**

```bash
cd backend
pip install PyJWT cryptography python-multipart
pip install -r requirements.txt
```

**Cấu hình môi trường (.env):**

```bash
# Supabase
SUPABASE_URL=https://<project-id>.supabase.co
SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
SUPABASE_JWT_SECRET=<jwt-secret>

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Auth
JWT_ALGORITHM=RS256
JWT_PUBLIC_KEY_URL=https://<project-id>.supabase.co/auth/v1/jwks
WEBHOOK_SECRET=<supabase-webhook-secret>
```

**Setup database:**

```bash
alembic upgrade head
```

## Cấu Trúc Mã

**Tổ chức module auth:**

```
backend/
├── app/
│   ├── core/
│   │   └── auth.py              # JWT verification, CurrentUser, role dependencies
│   ├── modules/
│   │   └── auth/
│   │       ├── __init__.py
│   │       ├── auth-models.py   # SQLModel: Profile, UserRole, AuditLog
│   │       ├── auth-schemas.py  # Pydantic: Request/Response schemas
│   │       ├── auth-service.py  # Business logic: assign_role, log_audit
│   │       ├── auth-routes.py   # FastAPI routes: /auth/me, /auth/roles
│   │       └── webhook.py       # Webhook handler cho Supabase
├── alembic/
│   └── versions/
│       └── 002_create_auth_tables.py
└── tests/
    └── test_auth/
        ├── test_jwt.py
        ├── test_roles.py
        └── test_audit.py
```

**Quy ước đặt tên:**

- Models: `PascalCase` (e.g., `UserRole`)
- Functions: `snake_case` (e.g., `verify_jwt_token`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `JWT_ALGORITHM`)
- Type hints: Dùng `X | None` thay vì `Optional[X]`

## Ghi Chú Triển Khai

### 1. JWT Verification Flow

**Core concept:**

```python
# app/core/auth.py
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, Header
from sqlmodel import Session, select
from app.core.config import settings
from app.modules.auth.auth-models import UserRole, Profile

# Step 1: Get Supabase public key (cached)
def get_supabase_public_key() -> str:
    """
    Fetch Supabase JWT public key from JWKS endpoint.
    Cache trong Redis với TTL 24h.
    """
    jwks_client = PyJWKClient(settings.JWT_PUBLIC_KEY_URL)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return signing_key.key

# Step 2: Verify JWT token
def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT signature và extract payload.
    Raise HTTPException 401 nếu invalid.
    """
    try:
        public_key = get_supabase_public_key()
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token không hợp lệ")

# Step 3: Extract token from header
def extract_token_from_header(authorization: str | None) -> str:
    """Parse 'Bearer <token>' from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Thiếu Authorization header")
    return authorization.split(" ")[1]
```

**Caching strategy:**

- Cache public key trong Redis: `supabase:jwt:public_key`, TTL 24h
- Cache user roles: `user:{user_id}:roles`, TTL 15 phút
- Invalidate cache khi role changes

### 2. CurrentUser Dependency

**Implementation pattern:**

```python
# app/core/auth.py
from dataclasses import dataclass
import uuid

@dataclass
class CurrentUser:
    """Represents authenticated user with roles."""
    user_id: uuid.UUID
    email: str
    roles: list[str]
    profile: Profile | None = None

    def has_role(self, role: str) -> bool:
        """Check if user has specific role."""
        return role in self.roles

    def has_any_role(self, roles: list[str]) -> bool:
        """Check if user has at least one of the roles."""
        return any(r in self.roles for r in roles)

    def is_customer(self) -> bool:
        return self.has_role("customer")

    def is_staff(self) -> bool:
        return self.has_role("staff")

    def is_admin(self) -> bool:
        return self.has_role("admin")

async def get_current_user(
    authorization: str | None = Header(None),
    session: Session = Depends(get_session)
) -> CurrentUser:
    """
    Load authenticated user from JWT + DB.

    Flow:
    1. Extract token from header
    2. Verify JWT signature
    3. Load user roles from DB (or cache)
    4. Load profile if exists
    5. Return CurrentUser object
    """
    token = extract_token_from_header(authorization)
    payload = verify_jwt_token(token)

    user_id = uuid.UUID(payload["sub"])
    email = payload["email"]

    # Load roles from cache or DB
    roles = await get_user_roles_cached(user_id, session)

    # Load profile (optional)
    profile = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()

    return CurrentUser(
        user_id=user_id,
        email=email,
        roles=roles,
        profile=profile
    )
```

**Caching helper:**

```python
async def get_user_roles_cached(
    user_id: uuid.UUID,
    session: Session
) -> list[str]:
    """Get user roles from cache, fallback to DB."""
    cache_key = f"user:{user_id}:roles"

    # Try cache first
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Fallback to DB
    roles = session.exec(
        select(UserRole.role).where(UserRole.user_id == user_id)
    ).all()

    # Cache for 15 minutes
    await redis_client.setex(
        cache_key,
        900,  # 15 minutes
        json.dumps(roles)
    )

    return roles
```

### 3. Role-Based Dependencies

**Factory pattern:**

```python
# app/core/auth.py
def require_role(required_role: str):
    """Factory function tạo dependency cho role check."""
    async def role_dependency(
        current_user: CurrentUser = Depends(get_current_user)
    ) -> CurrentUser:
        if not current_user.has_role(required_role):
            raise HTTPException(
                403,
                f"Yêu cầu quyền {required_role}"
            )
        return current_user
    return role_dependency

def require_roles(required_roles: list[str]):
    """Require at least one of the roles (OR logic)."""
    async def role_dependency(
        current_user: CurrentUser = Depends(get_current_user)
    ) -> CurrentUser:
        if not current_user.has_any_role(required_roles):
            raise HTTPException(
                403,
                f"Yêu cầu một trong các quyền: {', '.join(required_roles)}"
            )
        return current_user
    return role_dependency

# Shortcuts
require_customer = require_role("customer")
require_staff = require_role("staff")
require_admin = require_role("admin")
```

**Usage trong routes:**

```python
# app/modules/auth/auth-routes.py
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user, require_admin, CurrentUser

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me")
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    """Endpoint public cho authenticated users."""
    return {
        "user_id": str(current_user.user_id),
        "email": current_user.email,
        "roles": current_user.roles
    }

@router.post("/roles")
async def assign_role(
    request: AssignRoleRequest,
    current_user: CurrentUser = Depends(require_admin),
    session: Session = Depends(get_session)
):
    """Admin-only endpoint."""
    # ... implementation
```

### 4. Audit Logging

**Service pattern:**

```python
# app/modules/auth/auth-service.py
from app.modules.auth.auth-models import AuditLog
import uuid
from datetime import datetime

def log_audit_event(
    user_id: uuid.UUID,
    event_type: str,
    metadata: dict,
    ip_address: str,
    user_agent: str,
    session: Session
):
    """
    Ghi audit log vào database.

    Event types:
    - user.authenticated
    - user.logout
    - role.assigned
    - role.revoked
    - user.created
    """
    audit_log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent,
        created_at=datetime.utcnow()
    )
    session.add(audit_log)
    session.commit()
```

**Integration points:**

```python
# In get_current_user dependency
async def get_current_user(...):
    # ... verify JWT ...

    # Log authentication event
    log_audit_event(
        user_id=user_id,
        event_type="user.authenticated",
        metadata={"email": email},
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent"),
        session=session
    )

    return current_user
```

### 5. Webhook Handler

**Idempotent pattern:**

```python
# app/modules/auth/webhook.py
import hmac
import hashlib
from fastapi import Request, HTTPException

def verify_supabase_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:
    """Verify HMAC signature từ Supabase webhook."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

async def handle_user_created(
    user_data: dict,
    session: Session
) -> dict:
    """
    Handle Supabase webhook khi user mới đăng ký.
    Idempotent: Kiểm tra nếu profile đã tồn tại.
    """
    user_id = uuid.UUID(user_data["id"])
    email = user_data["email"]

    # Check if profile exists (idempotent)
    existing = session.exec(
        select(Profile).where(Profile.user_id == user_id)
    ).first()

    if existing:
        return {"message": "Profile already exists", "user_id": str(user_id)}

    # Create profile
    profile = Profile(
        user_id=user_id,
        full_name=email.split("@")[0],  # Default name
    )
    session.add(profile)

    # Assign customer role
    user_role = UserRole(
        user_id=user_id,
        role="customer"
    )
    session.add(user_role)

    # Log event
    log_audit_event(
        user_id=user_id,
        event_type="user.created",
        metadata={"email": email},
        ip_address="webhook",
        user_agent="supabase-webhook",
        session=session
    )

    session.commit()

    return {"message": "Profile created", "user_id": str(user_id)}
```

## Mẫu & Thực Tiễn Tốt Nhất

### Error Handling

**Consistent error responses:**

```python
# app/common/schemas.py
class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: dict | None = None

# Usage
raise HTTPException(
    status_code=401,
    detail={
        "error_code": "UNAUTHORIZED",
        "message": "Token không hợp lệ"
    }
)
```

### Type Hints (Python 3.13+)

**Modern syntax:**

```python
# ✅ Đúng
def get_profile(user_id: uuid.UUID) -> Profile | None:
    return session.exec(...).first()

# ❌ Tránh
from typing import Optional
def get_profile(user_id: uuid.UUID) -> Optional[Profile]:
    return session.exec(...).first()
```

### SQLModel Query Pattern

**Tuân thủ 100% SQLModel:**

```python
# ✅ Đúng
from sqlmodel import select

roles = session.exec(
    select(UserRole).where(UserRole.user_id == user_id)
).all()

# ❌ Tránh (raw SQL)
from sqlalchemy import text
roles = session.exec(text("SELECT * FROM user_roles WHERE ..."))
```

## Điểm Tích Hợp

### 1. Register Router

**Update `app/api/router.py`:**

```python
from fastapi import APIRouter
from app.modules.auth.auth-routes import router as auth_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
```

### 2. Database Connection

**Dùng sync Session:**

```python
from app.core.database import get_session

@router.get("/me")
async def get_me(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Use session for queries
    pass
```

### 3. Redis Connection

**Graceful fallback:**

```python
try:
    redis_client = get_redis_client()
    cached = await redis_client.get(key)
except Exception as e:
    logger.warning(f"Redis unavailable: {e}")
    cached = None  # Fallback to DB
```

## Xử Lý Lỗi

**Centralized exception handling:**

```python
# app/main.py
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.detail.get("error_code", "ERROR"),
            "message": exc.detail.get("message", str(exc.detail))
        }
    )
```

**Logging pattern:**

```python
import logging

logger = logging.getLogger(__name__)

try:
    # ... operation ...
except Exception as e:
    logger.error(f"Failed to verify JWT: {e}", exc_info=True)
    raise HTTPException(401, "Token verification failed")
```

## Cân Nhắc Hiệu Suất

### 1. Caching Strategy

**Multi-level cache:**

```
Request → In-memory cache → Redis → Database
```

**Implementation:**

```python
# In-memory cache cho public key (lru_cache)
from functools import lru_cache

@lru_cache(maxsize=1)
def get_cached_public_key() -> str:
    return fetch_from_supabase()

# Redis cache cho user roles
# (xem get_user_roles_cached ở trên)
```

### 2. Database Indexes

**Ensure indexes exist:**

```sql
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role);
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
```

### 3. Query Optimization

**Avoid N+1 queries:**

```python
# ✅ Good: Single query
roles = session.exec(
    select(UserRole).where(UserRole.user_id.in_(user_ids))
).all()

# ❌ Bad: N queries
for user_id in user_ids:
    roles = session.exec(
        select(UserRole).where(UserRole.user_id == user_id)
    ).all()
```

## Ghi Chú Bảo Mật

### 1. JWT Security

**Best practices:**

- ✅ Always verify signature
- ✅ Check expiry (`exp` claim)
- ✅ Validate issuer (`iss` claim)
- ✅ Use HTTPS only in production
- ❌ Never trust client-decoded JWT without verification

### 2. Webhook Security

**Verify signatures:**

```python
signature = request.headers.get("X-Supabase-Signature")
payload = await request.body()

if not verify_supabase_signature(payload, signature, settings.WEBHOOK_SECRET):
    raise HTTPException(401, "Invalid webhook signature")
```

### 3. Rate Limiting

**Add middleware:**

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/roles")
@limiter.limit("10/minute")
async def assign_role(...):
    pass
```

### 4. Input Validation

**Use Pydantic validators:**

```python
class AssignRoleRequest(BaseModel):
    user_id: uuid.UUID
    role: str = Field(..., pattern="^(customer|staff|admin)$")

    @validator("role")
    def validate_role(cls, v):
        if v not in ["customer", "staff", "admin"]:
            raise ValueError("Invalid role")
        return v
```
