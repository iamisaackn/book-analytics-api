# API key auth dependency
"""
API Key authentication dependency.

Mirrors the JWT Bearer pattern from production — same FastAPI Depends() structure,
same 401/403 error responses — just using a static API key instead of Keycloak
so the project runs standalone without an IAM server.

In production, swap get_current_user() for full JWT verification.
"""
import logging

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

logger = logging.getLogger(__name__)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(api_key: str = Security(api_key_header)) -> dict:
    """
    Validates the API key from the X-API-Key header.
    Returns a user claims dict — same shape as a decoded JWT would return,
    making it easy to swap in real JWT auth later.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Pass X-API-Key header.",
        )
    if api_key != settings.API_KEY:
        logger.warning("Invalid API key attempt")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )
    return {"sub": "api-user", "role": "admin"}