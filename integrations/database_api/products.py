"""Product endpoints."""
from typing import Dict, Any, Optional, List

from integrations.database_api.client import DatabaseAPIClient
from shared.logger import get_logger

logger = get_logger(__name__)


class ProductAPI:
    """Product data API."""
    
    def __init__(self, client: DatabaseAPIClient):
        """Initialize product API."""
        self.client = client
    
    async def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get product by ID.
        
        Args:
            product_id: Product identifier
        
        Returns:
            Product data or None
        """
        try:
            return await self.client.get(f"/products/{product_id}")
        except Exception as e:
            logger.error(f"Error fetching product: {str(e)}")
            return None
    
    async def search_products(
        self,
        query: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search products.
        
        Args:
            query: Search query
            category: Filter by category
        
        Returns:
            List of matching products
        """
        try:
            params = {"q": query}
            if category:
                params["category"] = category
            
            result = await self.client.get("/products/search", params=params)
            return result.get("results", [])
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []
    
    async def get_product_recommendations(
        self,
        customer_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get product recommendations for customer.
        
        Args:
            customer_id: Customer identifier
        
        Returns:
            List of recommended products
        """
        try:
            result = await self.client.get(
                f"/products/recommendations/{customer_id}"
            )
            return result.get("recommendations", [])
        except Exception as e:
            logger.error(f"Error fetching recommendations: {str(e)}")
            return []
