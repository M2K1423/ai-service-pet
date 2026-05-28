"""Product endpoints."""
from typing import Dict, Any, Optional, List

from integrations.database_api.client import DatabaseAPIClient
from shared.logger import get_logger

logger = get_logger(__name__)


class ProductAPI:
    """Product data API for PetCare (Medicines & Clinic Services)."""
    
    def __init__(self, client: DatabaseAPIClient):
        """Initialize product API."""
        self.client = client
    
    async def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get product/medicine by ID.
        """
        try:
            # We fetch from medicines list and find by ID
            result = await self.client.get(f"/api/ai-tools/medicines")
            items = result.get("items", [])
            for item in items:
                if str(item.get("id")) == str(product_id):
                    return item
            return None
        except Exception as e:
            logger.error(f"Error fetching product: {str(e)}")
            return None
    
    async def search_products(
        self,
        query: str,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search medicines.
        """
        try:
            result = await self.client.get("/api/ai-tools/medicines")
            items = result.get("items", [])
            query_lower = query.lower()
            filtered = []
            for item in items:
                if query_lower in item.get("name", "").lower() or query_lower in item.get("description", "").lower():
                    filtered.append(item)
            return filtered
        except Exception as e:
            logger.error(f"Error searching medicines: {str(e)}")
            return []
    
    async def get_product_recommendations(
        self,
        customer_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get product recommendations.
        """
        return []
    
    async def get_all_products(
        self,
        division: str = "odeli",
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Get all medicines from PetCare.
        """
        try:
            params = {"limit": limit}
            logger.info("📊 Gọi API CRM PetCare: /api/ai-tools/medicines (tất cả thuốc)")
            result = await self.client.get("/api/ai-tools/medicines", params=params)
            logger.info(f"✅ Nhận được {len(result.get('items', []))} thuốc")
            return result
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy tất cả thuốc: {str(e)}")
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
        Get medicines sorted by price.
        """
        try:
            params = {
                "sort": sort_by,
                "order": order.upper(),
                "limit": limit
            }
            
            logger.info("=" * 80)
            logger.info(f"📊 GỌI API CRM DATABASE - Sắp xếp thuốc theo {sort_by} ({order.upper()})")
            logger.info("=" * 80)
            logger.info(f"🔗 URL: {self.client.base_url}/api/ai-tools/medicines")
            logger.info(f"📋 Params: {params}")
            
            result = await self.client.get("/api/ai-tools/medicines", params=params)
            
            logger.info("=" * 80)
            logger.info(f"✅ RESPONSE TỪ CRM DATABASE (Medicines)")
            logger.info("=" * 80)
            logger.info(f"📦 Số lượng thuốc: {len(result.get('items', []))}")
            logger.info(f"📊 Total: {result.get('total', 0)}")
            logger.info("=" * 80)
            
            return result
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy danh sách thuốc: {str(e)}")
            return {"items": [], "page": 1, "limit": limit, "total": 0}
    
    async def get_products_by_price_asc(
        self,
        division: str = "odeli",
        limit: int = 10,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get medicines sorted by price ascending (rẻ nhất).
        """
        return await self.get_products_sorted(
            division=division,
            sort_by="price",
            order="ASC",
            limit=limit,
            category=category
        )
    
    async def get_products_by_price_desc(
        self,
        division: str = "odeli",
        limit: int = 10,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get medicines sorted by price descending (đắt nhất).
        """
        return await self.get_products_sorted(
            division=division,
            sort_by="price",
            order="DESC",
            limit=limit,
            category=category
        )
    
    async def get_product_detail(
        self,
        division: str,
        product_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get product detail.
        """
        return await self.get_product(product_id)
    
    async def get_categories(
        self,
        division: str = "odeli"
    ) -> List[Dict[str, Any]]:
        """
        Get all clinic services (mapped from categories in the old system).
        """
        try:
            logger.info("📁 Lấy danh sách dịch vụ y tế của phòng khám")
            result = await self.client.get("/api/ai-tools/services")
            services = result.get("items", []) if isinstance(result, dict) else []
            logger.info(f"✅ Có {len(services)} dịch vụ khám")
            return services
        except Exception as e:
            logger.error(f"❌ Lỗi khi lấy danh mục dịch vụ: {str(e)}")
            return []
    
    async def get_promotions(
        self,
        division: str = "odeli"
    ) -> List[Dict[str, Any]]:
        """
        Get promotions (not used in PetCare).
        """
        return []
    
    async def get_promotion_details(
        self,
        division: str,
        order_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get promotion details (not used in PetCare).
        """
        return {}
    
    async def get_tags(
        self,
        division: str = "odeli"
    ) -> List[str]:
        """
        Get tags (not used in PetCare).
        """
        return []

