"""API key authentication middleware."""
from fastapi import Header, HTTPException, status
from typing import Optional
import os

from shared.logger import get_logger

logger = get_logger(__name__)


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
) -> str:
    """
    Verify API key from request header.
    
    Args:
        x_api_key: API key from header
    
    Returns:
        Validated API key
    
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not x_api_key:
        logger.warning("API key missing from request")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required"
        )
    
    # Get valid API keys from environment
    valid_keys = os.getenv("API_KEYS", "").split(",")
    
    if x_api_key not in valid_keys:
        logger.warning(f"Invalid API key attempted: {x_api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return x_api_key
