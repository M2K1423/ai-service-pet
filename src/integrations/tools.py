"""
Database API Integration Tools
Xử lý tất cả các API calls xuống CRM database
"""
from typing import Dict, Any, List
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# Database API configuration
DATABASE_API_URL = os.getenv("DATABASE_API_URL", "http://localhost:9000")
http_client = httpx.AsyncClient(timeout=30.0)

async def get_customer_info(customer_id: str) -> Dict[str, Any]:
    """Lấy thông tin khách hàng."""
    # TODO: Call database API
    return {"customer_id": customer_id, "name": "Nguyễn Văn A"}

async def search_products(query: str = "", limit: int = 10, sort_by: str = "price", order: str = "ASC") -> List[Dict]:
    """Tìm kiếm sản phẩm theo giá."""
    try:
        params = {
            "sort": sort_by,
            "order": order.upper(),
            "limit": limit
        }
        print(f"📊 [TOOL] search_products called")
        print(f"   URL: {DATABASE_API_URL}/odeli/products")
        print(f"   Params: {params}")
        
        response = await http_client.get(
            f"{DATABASE_API_URL}/odeli/products",
            params=params
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        print(f"   📦 Items count: {len(result.get('items', []))}")
        
        items = result.get("items", [])
        # Format for display
        formatted_items = []
        for item in items[:limit]:
            formatted_items.append({
                "name": item.get("name", "N/A"),
                "price": item.get("price", 0),
                "sku": item.get("sku", "N/A"),
                "description": item.get("shortDescription", "")[:100]
            })
        print(f"   📋 Formatted {len(formatted_items)} items")
        return formatted_items
    except Exception as e:
        print(f"   ❌ Error fetching products: {e}")
        return []

async def get_all_products(limit: int = 20) -> List[Dict]:
    """Lấy tất cả sản phẩm."""
    try:
        print(f"📊 [TOOL] get_all_products called")
        print(f"   URL: {DATABASE_API_URL}/odeli/products")
        print(f"   Limit: {limit}")
        
        response = await http_client.get(
            f"{DATABASE_API_URL}/odeli/products",
            params={"limit": limit}
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        print(f"   📦 Items count: {len(result.get('items', []))}")
        
        items = result.get("items", [])
        formatted_items = []
        for item in items:
            formatted_items.append({
                "name": item.get("name", "N/A"),
                "price": item.get("price", 0),
                "sku": item.get("sku", "N/A"),
                "description": item.get("shortDescription", "")[:100]
            })
        print(f"   📋 Formatted {len(formatted_items)} items")
        return formatted_items
    except Exception as e:
        print(f"   ❌ Error fetching all products: {e}")
        return []

async def get_categories() -> List[Dict]:
    """Lấy danh mục sản phẩm."""
    try:
        print(f"📁 [TOOL] get_categories called")
        print(f"   URL: {DATABASE_API_URL}/odeli/categories")
        
        response = await http_client.get(f"{DATABASE_API_URL}/odeli/categories")
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        categories = result if isinstance(result, list) else result.get("items", [])
        formatted = [{"name": cat.get("name", "N/A"), "description": cat.get("description", "")} 
                for cat in categories]
        
        print(f"   📋 Categories count: {len(formatted)}")
        return formatted
    except Exception as e:
        print(f"   ❌ Error fetching categories: {e}")
        return []

async def get_promotions() -> List[Dict]:
    """Lấy khuyến mãi."""
    try:
        print(f"🎁 [TOOL] get_promotions called")
        print(f"   URL: {DATABASE_API_URL}/odeli/promotions")
        
        response = await http_client.get(f"{DATABASE_API_URL}/odeli/promotions")
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        promotions = result if isinstance(result, list) else result.get("items", [])
        formatted = [{"name": promo.get("name", "N/A"), "description": promo.get("description", "")} 
                for promo in promotions]
        
        print(f"   🎁 Promotions count: {len(formatted)}")
        return formatted
    except Exception as e:
        print(f"   ❌ Error fetching promotions: {e}")
        return []

async def get_order_status(order_id: str) -> Dict[str, Any]:
    """Kiểm tra đơn hàng."""
    # TODO: Call order API
    return {"order_id": order_id, "status": "Đang giao"}
