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
    
    async def get_all_products(
        self,
        division: str = "odeli",
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get all products from division.
        
        Args:
            division: Division identifier
            limit: Maximum products to return
        
        Returns:
            Dict with items, page, limit, total
        """
        try:
            params = {"limit": limit}
            
            logger.info(f"📊 Gọi API CRM: /{division}/products (tất cả sản phẩm)")
            result = await self.client.get(f"/{division}/products", params=params)
            logger.info(f"✅ Nhận được {len(result.get('items', []))} sản phẩm")
            return result
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy tất cả sản phẩm: {str(e)}")
            return {"items": [], "page": 1, "limit": limit, "total": 0}
    
    async def get_products_sorted(
        self,
        division: str = "your-division",
        sort_by: str = "price",
        order: str = "ASC",
        limit: int = 10,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get products sorted by price or other criteria.
        
        Args:
            division: Division identifier
            sort_by: Field to sort by (price, name, etc.)
            order: Sort order (ASC or DESC)
            limit: Maximum products to return
            category: Filter by category
        
        Returns:
            Dict with items, page, limit, total, category
        """
        try:
            params = {
                "sort": sort_by,
                "order": order.upper(),
                "limit": limit
            }
            if category:
                params["category"] = category
            
            logger.info("=" * 80)
            logger.info(f"📊 GỌI API CRM DATABASE")
            logger.info("=" * 80)
            logger.info(f"🔗 URL: {self.client.base_url}/{division}/products")
            logger.info(f"📋 Params: {params}")
            
            result = await self.client.get(f"/{division}/products", params=params)
            
            logger.info("=" * 80)
            logger.info(f"✅ RESPONSE TỪ CRM DATABASE")
            logger.info("=" * 80)
            logger.info(f"📦 Số lượng sản phẩm: {len(result.get('items', []))}")
            logger.info(f"📊 Total: {result.get('total', 0)}")
            logger.info(f"📄 Page: {result.get('page', 1)}")
            logger.info(f"🔢 Limit: {result.get('limit', 0)}")
            
            # Log chi tiết 3 sản phẩm đầu để kiểm tra
            items = result.get('items', [])
            if items:
                logger.info(f"📝 SAMPLE DATA (3 sản phẩm đầu):")
                import json
                for idx, item in enumerate(items[:3], 1):
                    logger.info(f"  [{idx}] {json.dumps(item, ensure_ascii=False, indent=4)}")
            logger.info("=" * 80)
            
            return result
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy danh sách sản phẩm: {str(e)}")
            return {"items": [], "page": 1, "limit": limit, "total": 0}
    
    async def get_product_detail(
        self,
        division: str,
        product_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get product detail by ID.
        
        Args:
            division: Division identifier
            product_id: Product ID
        
        Returns:
            Product detail or None
        """
        try:
            logger.info(f"📦 Lấy chi tiết sản phẩm: {product_id}")
            result = await self.client.get(f"/{division}/products/{product_id}")
            logger.info(f"✅ Nhận được chi tiết sản phẩm: {result.get('name', 'N/A')}")
            return result
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy chi tiết sản phẩm: {str(e)}")
            return None
    
    async def get_categories(
        self,
        division: str = "odeli"
    ) -> List[Dict[str, Any]]:
        """
        Get all product categories.
        
        Args:
            division: Division identifier
        
        Returns:
            List of categories
        """
        try:
            logger.info(f"📁 Lấy danh sách danh mục")
            result = await self.client.get(f"/{division}/categories")
            categories = result if isinstance(result, list) else result.get("items", [])
            logger.info(f"✅ Có {len(categories)} danh mục")
            return categories
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy danh mục: {str(e)}")
            return []
    
    async def get_promotions(
        self,
        division: str = "odeli"
    ) -> List[Dict[str, Any]]:
        """
        Get all promotions and combos.
        
        Args:
            division: Division identifier
        
        Returns:
            List of promotions
        """
        try:
            logger.info(f"🎁 Lấy danh sách khuyến mãi")
            result = await self.client.get(f"/{division}/promotions")
            promotions = result if isinstance(result, list) else result.get("items", [])
            logger.info(f"✅ Có {len(promotions)} khuyến mãi")
            return promotions
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy khuyến mãi: {str(e)}")
            return []
    
    async def get_promotion_details(
        self,
        division: str,
        order_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get promotion details by order.
        
        Args:
            division: Division identifier
            order_data: Order information to check applicable promotions
        
        Returns:
            Promotion details
        """
        try:
            logger.info(f"🎁 Lấy chi tiết khuyến mãi theo order")
            result = await self.client.post(
                f"/{division}/promotions/details",
                json_data=order_data
            )
            logger.info(f"✅ Nhận được chi tiết khuyến mãi")
            return result
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy chi tiết khuyến mãi: {str(e)}")
            return {}
    
    async def get_tags(
        self,
        division: str = "odeli"
    ) -> List[str]:
        """
        Get all product tags.
        
        Args:
            division: Division identifier
        
        Returns:
            List of tags
        """
        try:
            logger.info(f"🏷️ Lấy danh sách tags")
            result = await self.client.get(f"/{division}/tags")
            tags = result if isinstance(result, list) else result.get("items", [])
            logger.info(f"✅ Có {len(tags)} tags")
            return tags
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy tags: {str(e)}")
            return []
