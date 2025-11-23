"""Xác thực JWT từ Supabase và quản lý roles."""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWKClient, decode

from app.core.config import settings

# auto_error=False để cho phép check cookie nếu header không có
oauth2_scheme = HTTPBearer(auto_error=False)


def verify_jwt(token: str) -> dict:
    """Verify JWT từ Supabase và trả về payload."""
    try:
        if settings.debug:
            # Skip verify in dev mode
            payload = decode(token, options={"verify_signature": False})
        else:
            jwks_url = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"
            jwks_client = PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            payload = decode(
                token, signing_key.key, algorithms=["RS256"], audience="authenticated"
            )
        return payload
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
    user = {
        "id": payload["sub"],
        "email": payload.get("email"),
        "full_name": payload.get("user_metadata", {}).get("full_name"),
    }
    return user
