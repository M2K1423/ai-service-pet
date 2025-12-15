"""Request logging middleware."""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

from shared.logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Log request and response details."""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host}"
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} "
            f"processed in {process_time:.3f}s"
        )
        
        # Add process time header
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
