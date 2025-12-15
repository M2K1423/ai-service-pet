"""Input validation utilities."""
import re
from typing import Optional


def validate_phone_number(phone: str) -> bool:
    """
    Validate Vietnamese phone number.
    
    Args:
        phone: Phone number to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^(0|\+84)(3|5|7|8|9)\d{8}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """
    Validate email address.
    
    Args:
        email: Email to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_message(message: str) -> str:
    """
    Sanitize user message to prevent injection attacks.
    
    Args:
        message: Raw user message
    
    Returns:
        Sanitized message
    """
    # Remove HTML tags
    message = re.sub(r'<[^>]+>', '', message)
    
    # Remove special characters that could be malicious
    message = message.strip()
    
    return message


def validate_session_id(session_id: Optional[str]) -> bool:
    """
    Validate session ID format.
    
    Args:
        session_id: Session ID to validate
    
    Returns:
        True if valid or None, False otherwise
    """
    if session_id is None:
        return True
    
    # Session ID should be alphanumeric with optional hyphens/underscores
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, session_id))
