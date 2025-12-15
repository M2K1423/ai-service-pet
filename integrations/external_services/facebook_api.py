"""Facebook Messenger API integration."""
from typing import Dict, Any, Optional
import httpx

from shared.logger import get_logger

logger = get_logger(__name__)


class FacebookAPI:
    """Client for Facebook Messenger API."""
    
    def __init__(
        self,
        page_access_token: Optional[str] = None,
        verify_token: Optional[str] = None
    ):
        """
        Initialize Facebook API client.
        
        Args:
            page_access_token: Facebook Page access token
            verify_token: Webhook verify token
        """
        self.page_access_token = page_access_token
        self.verify_token = verify_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.client = httpx.AsyncClient()
    
    async def send_message(
        self,
        recipient_id: str,
        message: str,
        messaging_type: str = "RESPONSE"
    ) -> Dict[str, Any]:
        """
        Send message to Facebook user.
        
        Args:
            recipient_id: Facebook user ID
            message: Message content
            messaging_type: Message type
        
        Returns:
            API response
        """
        try:
            url = f"{self.base_url}/me/messages"
            
            params = {
                "access_token": self.page_access_token
            }
            
            data = {
                "messaging_type": messaging_type,
                "recipient": {
                    "id": recipient_id
                },
                "message": {
                    "text": message
                }
            }
            
            response = await self.client.post(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Facebook API error: {str(e)}")
            raise
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get Facebook user profile.
        
        Args:
            user_id: Facebook user ID
        
        Returns:
            User profile information
        """
        try:
            url = f"{self.base_url}/{user_id}"
            
            params = {
                "access_token": self.page_access_token,
                "fields": "first_name,last_name,profile_pic"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return None
    
    def verify_webhook(
        self,
        mode: str,
        token: str,
        challenge: str
    ) -> Optional[str]:
        """
        Verify Facebook webhook.
        
        Args:
            mode: Verification mode
            token: Verification token
            challenge: Challenge string
        
        Returns:
            Challenge if verified, None otherwise
        """
        if mode == "subscribe" and token == self.verify_token:
            logger.info("Facebook webhook verified")
            return challenge
        
        logger.warning("Facebook webhook verification failed")
        return None
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
