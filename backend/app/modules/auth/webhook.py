"""
Webhook handlers cho Supabase events.
Xử lý các events từ Supabase như user.created, user.updated, etc.
"""

import hmac
import hashlib
import logging
from typing import Any

from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


def verify_supabase_signature(
    payload: bytes,
    signature: str | None,
    secret: str,
) -> None:
    """
    Verify HMAC signature từ Supabase webhook.
    
    Args:
        payload: Raw request body (bytes)
        signature: X-Supabase-Signature header value
        secret: Webhook secret từ Supabase dashboard
        
    Raises:
        HTTPException 401: Nếu signature không hợp lệ
    """
    if not signature:
        logger.warning("Webhook request thiếu X-Supabase-Signature header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiếu signature header",
        )
    
    # Tính HMAC SHA256
    expected_signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    
    # So sánh signature (constant-time để tránh timing attack)
    if not hmac.compare_digest(signature, expected_signature):
        logger.warning("Webhook signature không hợp lệ")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature không hợp lệ",
        )
    
    logger.debug("Webhook signature verified thành công")


def extract_user_data_from_record(record: dict[str, Any]) -> dict[str, Any]:
    """
    Extract user data từ Supabase webhook record.
    
    Args:
        record: User record từ webhook payload
        
    Returns:
        Dict chứa user_id, email, metadata
    """
    return {
        "user_id": record.get("id"),
        "email": record.get("email"),
        "email_confirmed_at": record.get("email_confirmed_at"),
        "created_at": record.get("created_at"),
        "user_metadata": record.get("raw_user_meta_data", {}),
        "app_metadata": record.get("raw_app_meta_data", {}),
    }


def validate_webhook_payload(payload: dict[str, Any]) -> None:
    """
    Validate webhook payload structure.
    
    Args:
        payload: Webhook payload từ Supabase
        
    Raises:
        HTTPException 400: Nếu payload không hợp lệ
    """
    required_fields = ["type", "table", "record", "schema"]
    
    for field in required_fields:
        if field not in payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Webhook payload thiếu field '{field}'",
            )
    
    # Validate type
    if payload["type"] not in ["INSERT", "UPDATE", "DELETE"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook type '{payload['type']}' không hợp lệ",
        )
    
    # Validate table
    if payload["table"] != "users":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook table '{payload['table']}' không được hỗ trợ",
        )
    
    # Validate schema
    if payload["schema"] != "auth":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook schema '{payload['schema']}' không hợp lệ",
        )
