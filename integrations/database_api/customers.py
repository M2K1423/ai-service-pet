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
        Get customer by ID.
        
        Args:
            customer_id: Customer identifier
        
        Returns:
            Customer data or None
        """
        try:
            return await self.client.get(f"/customers/{customer_id}")
        except Exception as e:
            logger.error(f"Error fetching customer: {str(e)}")
            return None
    
    async def search_customers(self, query: str) -> list:
        """
        Search customers.
        
        Args:
            query: Search query
        
        Returns:
            List of matching customers
        """
        try:
            result = await self.client.get("/customers/search", params={"q": query})
            return result.get("results", [])
        except Exception as e:
            logger.error(f"Error searching customers: {str(e)}")
            return []
    
    async def create_customer(self, customer_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create new customer.
        
        Args:
            customer_data: Customer information
        
        Returns:
            Created customer data
        """
        try:
            return await self.client.post("/customers", json_data=customer_data)
        except Exception as e:
            logger.error(f"Error creating customer: {str(e)}")
            return None
