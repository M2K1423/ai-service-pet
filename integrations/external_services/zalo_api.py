"""Zalo OA API integration."""
from typing import Dict, Any, Optional
import httpx

from shared.logger import get_logger

logger = get_logger(__name__)


class ZaloAPI:
    """Client for Zalo Official Account API."""
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Zalo API client.
        
        Args:
            access_token: Zalo OA access token
        """
        self.access_token = access_token
        self.base_url = "https://openapi.zalo.me/v2.0"
        self.client = httpx.AsyncClient()
    
    async def send_message(
        self,
        user_id: str,
        message: str,
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Send message to Zalo user.
        
        Args:
            user_id: Zalo user ID
            message: Message content
            message_type: Message type (text, image, etc.)
        
        Returns:
            API response
        """
        try:
            url = f"{self.base_url}/oa/message"
            
            headers = {
                "access_token": self.access_token,
                "Content-Type": "application/json"
            }
            
            data = {
                "recipient": {
                    "user_id": user_id
                },
                "message": {
                    "text": message
                }
            }
            
            response = await self.client.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Zalo API error: {str(e)}")
            raise
    
    async def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get Zalo user information.
        
        Args:
            user_id: Zalo user ID
        
        Returns:
            User information
        """
        try:
            url = f"{self.base_url}/oa/getprofile"
            
            params = {
                "access_token": self.access_token,
                "data": {
                    "user_id": user_id
                }
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Zalo API error: {str(e)}")
            return None
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
