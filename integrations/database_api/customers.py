"""Customer endpoints."""
from typing import Dict, Any, Optional

from integrations.database_api.client import DatabaseAPIClient
from shared.logger import get_logger

logger = get_logger(__name__)


class CustomerAPI:
    """Customer data API."""
    
    def __init__(self, client: DatabaseAPIClient):
        """Initialize customer API."""
        self.client = client
    
    async def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get customer and pet info by ID from PetCare.
        
        Args:
            customer_id: Customer identifier (e.g. owner_1)
        
        Returns:
            Customer and pet data or None
        """
        try:
            # PetCare endpoint: /api/ai-tools/customer-info/{id}
            return await self.client.get(f"/api/ai-tools/customer-info/{customer_id}")
        except Exception as e:
            logger.error(f"Error fetching customer from PetCare: {str(e)}")
            return None
    
    async def get_appointments(self, customer_id: str) -> list:
        """
        Get customer appointments from PetCare.
        """
        try:
            result = await self.client.get(f"/api/ai-tools/appointments/{customer_id}")
            return result.get("appointments", [])
        except Exception as e:
            logger.error(f"Error fetching appointments: {str(e)}")
            return []
