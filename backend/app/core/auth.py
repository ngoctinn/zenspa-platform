"""
Xác thực và phân quyền JWT từ Supabase.
Cung cấp dependencies để verify token, load user info và kiểm tra roles.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Any

import jwt
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.redis.client import get_redis_client

logger = logging.getLogger(__name__)

# Security scheme để extract Bearer token từ header
security = HTTPBearer()


def extract_token_from_header(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Trích xuất JWT token từ Authorization header.
    
    Args:
        credentials: HTTP Bearer credentials từ header
        
    Returns:
        JWT token string
        
    Raises:
        HTTPException 401: Nếu token format không hợp lệ
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiếu token xác thực",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials


def get_supabase_public_key() -> str:
    """
    Lấy public key từ Supabase JWKS endpoint để verify JWT signature.
    Cache key trong Redis với TTL 1 giờ.
    
    Returns:
        RSA public key string (PEM format)
        
    Raises:
        HTTPException 500: Nếu không thể lấy public key từ Supabase
    """
    redis_client = get_redis_client()
    cache_key = "supabase:jwks:public_key"
    
    # Kiểm tra cache trước
    cached_key = redis_client.get(cache_key)
    if cached_key:
        logger.debug("Sử dụng Supabase public key từ cache")
        return cached_key
    
    # Fetch từ Supabase JWKS endpoint
    try:
        # Extract project URL từ database_url
        # Format: postgresql://user:pass@db.PROJECT_ID.supabase.co:5432/postgres
        # Hoặc lấy từ SUPABASE_URL env var
        supabase_url = getattr(settings, "supabase_url", None)
        if not supabase_url:
            # Fallback: extract từ database_url
            db_url = settings.database_url
            # Parse hostname: db.PROJECT_ID.supabase.co → https://PROJECT_ID.supabase.co
            if "supabase.co" in db_url:
                parts = db_url.split("@")[1].split(":")[0]  # db.PROJECT_ID.supabase.co
                project_id = parts.split(".")[1]  # PROJECT_ID
                supabase_url = f"https://{project_id}.supabase.co"
            else:
                raise ValueError("Không thể xác định Supabase URL từ database_url")
        
        jwks_url = f"{supabase_url}/auth/v1/jwks"
        logger.info(f"Fetching Supabase JWKS từ {jwks_url}")
        
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()
        
        jwks = response.json()
        
        # Lấy key đầu tiên (Supabase thường chỉ có 1 key)
        if not jwks.get("keys"):
            raise ValueError("JWKS response không chứa keys")
        
        key_data = jwks["keys"][0]
        
        # Convert JWK to PEM format
        from jwt.algorithms import RSAAlgorithm
        public_key = RSAAlgorithm.from_jwk(json.dumps(key_data))
        
        # Serialize to PEM
        from cryptography.hazmat.primitives import serialization
        pem_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        
        # Cache trong Redis (TTL 1 giờ)
        redis_client.setex(cache_key, 3600, pem_key)
        logger.info("Đã cache Supabase public key (TTL: 1h)")
        
        return pem_key
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi khi fetch JWKS từ Supabase: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể xác thực token (JWKS error)",
        )
    except (ValueError, KeyError) as e:
        logger.error(f"Lỗi khi parse JWKS response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi cấu hình xác thực (JWKS parse error)",
        )


def verify_jwt_token(token: str) -> dict[str, Any]:
    """
    Verify JWT signature và extract payload.
    
    Args:
        token: JWT token string
        
    Returns:
        Payload dict chứa user_id, email, exp, etc.
        
    Raises:
        HTTPException 401: Nếu token invalid/expired
    """
    try:
        # Lấy public key từ cache hoặc Supabase
        public_key = get_supabase_public_key()
        
        # Decode và verify
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_exp": True},
        )
        
        # Validate required claims
        if "sub" not in payload:
            raise ValueError("Token thiếu claim 'sub' (user_id)")
        
        logger.debug(f"Token verified thành công cho user: {payload.get('sub')}")
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token đã hết hạn")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Token không hợp lệ: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Lỗi không mong muốn khi verify token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Lỗi xác thực token",
        )


class CurrentUser:
    """
    Object chứa thông tin user hiện tại (từ JWT + DB).
    Dùng trong FastAPI dependencies.
    """
    
    def __init__(
        self,
        user_id: str,
        email: str,
        roles: list[str],
        profile: dict[str, Any] | None = None,
    ):
        """
        Khởi tạo CurrentUser.
        
        Args:
            user_id: UUID của user từ auth.users
            email: Email từ JWT payload
            roles: List các roles (customer, receptionist, technician, admin)
            profile: Profile data từ profiles table (optional)
        """
        self.user_id = user_id
        self.email = email
        self.roles = roles
        self.profile = profile
    
    def has_role(self, role: str) -> bool:
        """Kiểm tra user có role cụ thể không."""
        return role in self.roles
    
    def is_customer(self) -> bool:
        """Kiểm tra user có role customer không."""
        return "customer" in self.roles
    
    def is_receptionist(self) -> bool:
        """Kiểm tra user có role receptionist không."""
        return "receptionist" in self.roles
    
    def is_technician(self) -> bool:
        """Kiểm tra user có role technician không."""
        return "technician" in self.roles
    
    def is_admin(self) -> bool:
        """Kiểm tra user có role admin không."""
        return "admin" in self.roles
    
    def has_any_role(self, roles: list[str]) -> bool:
        """Kiểm tra user có ít nhất 1 trong các roles không."""
        return any(role in self.roles for role in roles)


async def get_current_user(
    token: str = Depends(extract_token_from_header),
    session: Session = Depends(get_session),
) -> CurrentUser:
    """
    FastAPI dependency: Load user info + roles từ JWT token.
    Cache user data trong Redis (TTL 15 phút).
    
    Args:
        token: JWT token từ Authorization header
        session: SQLModel session
        
    Returns:
        CurrentUser object với user info + roles
        
    Raises:
        HTTPException 401: Nếu token invalid hoặc user không tồn tại
    """
    # Verify JWT
    payload = verify_jwt_token(token)
    user_id = payload["sub"]
    email = payload.get("email", "")
    
    # Kiểm tra cache trước
    redis_client = get_redis_client()
    cache_key = f"user:{user_id}:roles"
    
    cached_data = redis_client.get(cache_key)
    if cached_data:
        try:
            data = json.loads(cached_data)
            logger.debug(f"Load user {user_id} từ cache")
            return CurrentUser(
                user_id=user_id,
                email=email,
                roles=data["roles"],
                profile=data.get("profile"),
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Cache data không hợp lệ, query DB: {e}")
    
    # Query roles từ DB
    from app.modules.auth.auth_models import UserRole, Profile
    
    # Load roles
    stmt = select(UserRole).where(UserRole.user_id == user_id)
    user_roles = session.exec(stmt).all()
    
    if not user_roles:
        logger.warning(f"User {user_id} không có roles nào")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User chưa được gán role",
        )
    
    roles = [ur.role for ur in user_roles]
    
    # Load profile (optional)
    profile_stmt = select(Profile).where(Profile.user_id == user_id)
    profile_obj = session.exec(profile_stmt).first()
    
    profile_data = None
    if profile_obj:
        profile_data = {
            "id": str(profile_obj.id),
            "full_name": profile_obj.full_name,
            "avatar_url": profile_obj.avatar_url,
        }
    
    # Cache trong Redis (TTL 15 phút)
    cache_data = {
        "roles": roles,
        "profile": profile_data,
    }
    redis_client.setex(cache_key, 900, json.dumps(cache_data))
    logger.debug(f"Đã cache user {user_id} roles (TTL: 15m)")
    
    return CurrentUser(
        user_id=user_id,
        email=email,
        roles=roles,
        profile=profile_data,
    )


def require_role(role: str):
    """
    Dependency factory: Yêu cầu user có role cụ thể.
    
    Args:
        role: Role cần kiểm tra (customer, receptionist, technician, admin)
        
    Returns:
        FastAPI dependency function
        
    Example:
        @router.get("/admin-only")
        async def admin_route(user: CurrentUser = Depends(require_role("admin"))):
            return {"message": "Admin area"}
    """
    async def check_role(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current_user.has_role(role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Yêu cầu role '{role}' để truy cập",
            )
        return current_user
    
    return check_role


def require_any_role(roles: list[str]):
    """
    Dependency factory: Yêu cầu user có ít nhất 1 trong các roles.
    
    Args:
        roles: List các roles được phép
        
    Returns:
        FastAPI dependency function
        
    Example:
        @router.get("/staff-area")
        async def staff_route(
            user: CurrentUser = Depends(require_any_role(["receptionist", "admin"]))
        ):
            return {"message": "Staff area"}
    """
    async def check_any_role(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current_user.has_any_role(roles):
            roles_str = ", ".join(roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Yêu cầu 1 trong các role: {roles_str}",
            )
        return current_user
    
    return check_any_role


# Shortcuts cho các roles phổ biến
async def require_customer(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dependency: Yêu cầu role customer."""
    if not current_user.is_customer():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ khách hàng mới được truy cập",
        )
    return current_user


async def require_receptionist(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dependency: Yêu cầu role receptionist."""
    if not current_user.is_receptionist():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ lễ tân mới được truy cập",
        )
    return current_user


async def require_technician(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dependency: Yêu cầu role technician."""
    if not current_user.is_technician():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ kỹ thuật viên mới được truy cập",
        )
    return current_user


async def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dependency: Yêu cầu role admin."""
    if not current_user.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới được truy cập",
        )
    return current_user


# Alias: require staff = receptionist hoặc admin
async def require_staff(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dependency: Yêu cầu role receptionist hoặc admin."""
    if not current_user.has_any_role(["receptionist", "admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ nhân viên (lễ tân hoặc admin) mới được truy cập",
        )
    return current_user
