"""Database API client."""
from typing import Dict, Any, Optional
import httpx

from shared.logger import get_logger

logger = get_logger(__name__)


class DatabaseAPIClient:
    """Client for internal database API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize database API client.
        
        Args:
            base_url: Base URL for database API
            api_key: API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            headers={"X-API-Key": api_key} if api_key else {},
            timeout=20.0
        )

    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make GET request to database API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
        
        Returns:
            API response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.info(f"🔗 DatabaseAPIClient GET: {url}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            import traceback
            logger.error(f"Database API error calling {url}: {repr(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    
    async def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make POST request to database API.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
        
        Returns:
            API response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = await self.client.post(url, data=data, json=json_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Database API error: {str(e)}")
            raise
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
