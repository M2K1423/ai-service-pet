"""Order endpoints."""
from typing import Dict, Any, Optional, List

from integrations.database_api.client import DatabaseAPIClient
from shared.logger import get_logger

logger = get_logger(__name__)


class OrderAPI:
    """Order data API."""
    
    def __init__(self, client: DatabaseAPIClient):
        """Initialize order API."""
        self.client = client
    
    async def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Get order by ID.
        
        Args:
            order_id: Order identifier
        
        Returns:
            Order data or None
        """
        try:
            return await self.client.get(f"/orders/{order_id}")
        except Exception as e:
            logger.error(f"Error fetching order: {str(e)}")
            return None
    
    async def get_customer_orders(
        self,
        customer_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get orders for customer.
        
        Args:
            customer_id: Customer identifier
            limit: Maximum orders to return
        
        Returns:
            List of orders
        """
        try:
            result = await self.client.get(
                f"/orders/customer/{customer_id}",
                params={"limit": limit}
            )
            return result.get("orders", [])
        except Exception as e:
            logger.error(f"Error fetching customer orders: {str(e)}")
            return []
    
    async def create_order(self, order_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create new order.
        
        Args:
            order_data: Order information
        
        Returns:
            Created order data
        """
        try:
            return await self.client.post("/orders", json_data=order_data)
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return None
    
    async def update_order_status(
        self,
        order_id: str,
        status: str
    ) -> Optional[Dict[str, Any]]:
        """
        Update order status.
        
        Args:
            order_id: Order identifier
            status: New status
        
        Returns:
            Updated order data
        """
        try:
            return await self.client.post(
                f"/orders/{order_id}/status",
                json_data={"status": status}
            )
        except Exception as e:
            logger.error(f"Error updating order status: {str(e)}")
            return None
