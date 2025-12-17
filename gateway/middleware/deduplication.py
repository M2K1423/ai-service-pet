"""Request deduplication middleware."""
import hashlib
import time
from typing import Dict, Tuple
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from shared.logger import get_logger

logger = get_logger(__name__)


class RequestDeduplicationMiddleware(BaseHTTPMiddleware):
    """Middleware to prevent duplicate requests."""
    
    def __init__(self, app, window_seconds: int = 30):
        """
        Initialize deduplication middleware.
        
        Args:
            app: FastAPI application
            window_seconds: Time window to check for duplicates (default: 30s)
        """
        super().__init__(app)
        self.window_seconds = window_seconds
        self.request_cache: Dict[str, Tuple[float, Response]] = {}
        
    def _generate_request_key(self, user_id: str, message: str, session_id: str) -> str:
        """
        Generate unique key for request.
        
        Args:
            user_id: User ID
            message: Message content
            session_id: Session ID
            
        Returns:
            Hash key for request
        """
        content = f"{user_id}:{message}:{session_id}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _cleanup_old_entries(self) -> None:
        """Remove expired entries from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, (timestamp, _) in self.request_cache.items()
            if current_time - timestamp > self.window_seconds
        ]
        for key in expired_keys:
            del self.request_cache[key]
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request with deduplication.
        
        Args:
            request: Incoming request
            call_next: Next middleware/route handler
            
        Returns:
            Response
        """
        # Only apply to chat endpoint
        if request.url.path != "/api/v1/chat" or request.method != "POST":
            return await call_next(request)
        
        try:
            # Read request body
            body = await request.body()
            
            # Parse JSON to get user_id, message, session_id
            import json
            data = json.loads(body.decode())
            user_id = data.get("user_id", "")
            message = data.get("message", "")
            session_id = data.get("session_id", "")
            
            # Generate request key
            request_key = self._generate_request_key(user_id, message, session_id)
            
            # Cleanup old entries
            self._cleanup_old_entries()
            
            # Check if duplicate
            current_time = time.time()
            if request_key in self.request_cache:
                cached_time, cached_response = self.request_cache[request_key]
                time_diff = current_time - cached_time
                
                logger.warning(
                    f"🚫 PHÁT HIỆN DUPLICATE REQUEST "
                    f"(user: {user_id}, message: {message[:50]}..., "
                    f"thời gian: {time_diff:.1f}s trước)"
                )
                
                # Return cached response
                return Response(
                    content=cached_response.body,
                    status_code=cached_response.status_code,
                    headers=dict(cached_response.headers),
                    media_type=cached_response.media_type
                )
            
            # Create new request with body (since we already read it)
            async def receive():
                return {"type": "http.request", "body": body}
            
            request._receive = receive
            
            # Process request
            response = await call_next(request)
            
            # Cache successful response
            if response.status_code == 200:
                # Read response body
                response_body = b""
                async for chunk in response.body_iterator:
                    response_body += chunk
                
                # Create cached response
                cached_response = Response(
                    content=response_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
                
                # Store in cache
                self.request_cache[request_key] = (current_time, cached_response)
                
                logger.info(
                    f"💾 ĐÃ LƯU CACHE CHO REQUEST "
                    f"(user: {user_id}, cache size: {len(self.request_cache)})"
                )
                
                # Return response with same body
                return Response(
                    content=response_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
            
            return response
            
        except Exception as e:
            logger.error(f"❌ LỖI DEDUPLICATION MIDDLEWARE: {str(e)}")
            return await call_next(request)
