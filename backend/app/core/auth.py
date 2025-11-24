"""Xác thực JWT từ Supabase và quản lý roles."""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode

from app.core.config import settings

# auto_error=False để cho phép check cookie nếu header không có
oauth2_scheme = HTTPBearer(auto_error=False)


def verify_jwt(token: str) -> dict:
    """Verify JWT từ Supabase và trả về payload."""
    try:
        if not settings.supabase_jwt_secret:
            raise Exception("Chưa cấu hình SUPABASE_JWT_SECRET")

        return decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
            leeway=60,  # Cho phép lệch 60s để tránh lỗi iat
        )
    except Exception as e:
        print(f"JWT verify error: {e}")  # Debug log
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token không hợp lệ"
        )


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
) -> dict:
    """Dependency để lấy thông tin cơ bản của user hiện tại từ JWT (Header hoặc Cookie)."""
    token = None

    # 1. Ưu tiên lấy từ Header Authorization
    if credentials:
        token = credentials.credentials

    # 2. Nếu không có header, lấy từ Cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không tìm thấy token xác thực",
        )

    payload = verify_jwt(token)

    # Lấy roles từ app_metadata (được inject bởi Supabase Auth Hook)
    app_metadata = payload.get("app_metadata", {})
    roles = app_metadata.get("roles", [])

    user = {
        "id": payload["sub"],
        "email": payload.get("email"),
        "full_name": payload.get("user_metadata", {}).get("full_name"),
        "roles": roles,
    }
    return user
