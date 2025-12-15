"""Custom exceptions."""


class AIServiceException(Exception):
    """Base exception for AI service."""
    pass


class AuthenticationError(AIServiceException):
    """Authentication error."""
    pass


class RateLimitError(AIServiceException):
    """Rate limit exceeded."""
    pass


class ValidationError(AIServiceException):
    """Validation error."""
    pass


class ExternalAPIError(AIServiceException):
    """External API error."""
    pass


class DatabaseError(AIServiceException):
    """Database error."""
    pass


class AgentError(AIServiceException):
    """Agent processing error."""
    pass


class ConfigurationError(AIServiceException):
    """Configuration error."""
    pass
