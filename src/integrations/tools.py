"""
Store API Integration Tools
Tools để Agno Agent gọi tới Store Backend API
Theo sơ đồ: AI Agent -> Store API (/odeli/products/xxx)
"""
from typing import Dict, Any, List, Optional
import httpx
from src.config.settings import settings

# HTTP Client với retry và timeout
http_client = httpx.AsyncClient(
    timeout=settings.HTTP_TIMEOUT,
    follow_redirects=True
)

async def get_customer_info(customer_id: str) -> Dict[str, Any]:
    """
    Lấy thông tin khách hàng từ Store API.
    
    Args:
        customer_id: ID khách hàng
        
    Returns:
        Dict với thông tin khách hàng
    """
    try:
        url = settings.get_customer_url(customer_id)
        print(f"👤 [TOOL] get_customer_info called")
        print(f"   URL: {url}")
        
        response = await http_client.get(url)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        return result
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        return {
            "customer_id": customer_id,
            "error": f"Customer not found: {e.response.status_code}"
        }
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {
            "customer_id": customer_id,
            "error": str(e)
        }

async def search_products(
    query: str = "", 
    limit: int = 10, 
    sort_by: Optional[str] = "price", 
    order: Optional[str] = "ASC",
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[Dict]:
    """
    Tìm kiếm sản phẩm từ Store API. 
    
    🎯 KHI NÀO SỬ DỤNG TOOL NÀY:
    - Khách hỏi về sản phẩm cụ thể: "tìm cà ri", "có bò né không", "show món gà"
    - Khách hỏi về giá: "sp rẻ nhất", "món dưới 50k", "đắt nhất"
    - Khách hỏi về danh mục: "có đồ uống gì", "món chính"
    - Bất kỳ câu hỏi nào về SẢN PHẨM, MÓN ĂN
    
    📋 CÁCH DÙNG PARAMETERS:
    
    Args:
        query (str): Từ khóa tìm kiếm - TÊN sản phẩm/món ăn
            • Ví dụ: "cà ri", "bò né", "gà rán", "trà sữa"
            • Dùng khi khách hỏi về SẢN PHẨM CỤ THỂ
            • Có thể để trống "" nếu chỉ lọc theo category/giá
            
        limit (int): Số lượng kết quả trả về (mặc định: 10)
            • Đề xuất: 5-10 sản phẩm cho dễ đọc
            
        sort_by (str): Sắp xếp theo trường nào
            • "price" - sắp xếp theo giá (PHỔ BIẾN NHẤT)
            • "name" - sắp xếp theo tên
            • "created_at" - sắp xếp theo ngày tạo
            
        order (str): Thứ tự sắp xếp
            • "ASC" - Tăng dần (rẻ → đắt, A → Z)
            • "DESC" - Giảm dần (đắt → rẻ, Z → A)
            
        category (str, optional): Lọc theo danh mục
            • Ví dụ: "beverages", "main_course", "dessert"
            • Dùng khi khách hỏi về LOẠI món chung chung
            
        min_price (float, optional): Giá tối thiểu (VND)
            • Ví dụ: 30000 (30k)
            
        max_price (float, optional): Giá tối đa (VND)
            • Ví dụ: 50000 (50k)
    
    💡 VÍ DỤ SỬ DỤNG:
        
        1. Khách hỏi: "cho tôi sp về cà ri"
           → search_products(query="cà ri", limit=5)
        
        2. Khách hỏi: "tìm món rẻ nhất"
           → search_products(sort_by="price", order="ASC", limit=5)
        
        3. Khách hỏi: "có đồ uống gì"
           → search_products(category="beverages", limit=5)
        
        4. Khách hỏi: "cà ri dưới 60k"
           → search_products(query="cà ri", max_price=60000, limit=5)
        
        5. Khách hỏi: "món từ 30-50k"
           → search_products(min_price=30000, max_price=50000, limit=5)
        
    Returns:
        List[Dict]: Danh sách sản phẩm, mỗi item có:
            - sku: Mã sản phẩm
            - name: Tên sản phẩm
            - price: Giá (VND)
            - category: Danh mục
            - description: Mô tả ngắn
            - stock: Số lượng tồn kho
            - image_url: Link hình ảnh
    """
    try:
        # Clean empty strings to None
        if min_price == "":
            min_price = None
        if max_price == "":
            max_price = None
        if category == "":
            category = None
        
        # Set defaults if None
        if sort_by is None or sort_by == "":
            sort_by = "price"
        if order is None or order == "":
            order = "ASC"
            
        # Build query params
        params = {
            "sort": sort_by,
            "order": order.upper(),
            "limit": limit
        }
        
        if query:
            params["q"] = query
        if category:
            params["category"] = category
        if min_price is not None and min_price > 0:
            params["min_price"] = min_price
        if max_price is not None and max_price > 0:
            params["max_price"] = max_price
            
        url = settings.get_product_url()
        print(f"🔍 [TOOL] search_products called")
        print(f"   URL: {url}")
        print(f"   Params: {params}")
        
        response = await http_client.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        items = result.get("items", []) if isinstance(result, dict) else result
        print(f"   📦 Items count: {len(items)}")
        
        # Format for Agent to understand
        formatted_items = []
        for item in items[:limit]:
            formatted_items.append({
                "sku": item.get("sku", "N/A"),
                "name": item.get("name", "N/A"),
                "price": item.get("price", 0),
                "category": item.get("category", ""),
                "description": item.get("shortDescription", "")[:150],
                "stock": item.get("stock", 0),
                "image_url": item.get("imageUrl", "")
            })
        
        print(f"   📋 Formatted {len(formatted_items)} items")
        return formatted_items
        
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        return []
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

async def get_product_detail(sku: str) -> Dict[str, Any]:
    """
    Lấy chi tiết một sản phẩm.
    
    Args:
        sku: Mã SKU của sản phẩm
        
    Returns:
        Dict với thông tin chi tiết sản phẩm
    """
    try:
        url = settings.get_product_url(sku)
        print(f"📦 [TOOL] get_product_detail called")
        print(f"   URL: {url}")
        print(f"   SKU: {sku}")
        
        response = await http_client.get(url)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        # Format detailed product info
        product = {
            "sku": result.get("sku", sku),
            "name": result.get("name", "N/A"),
            "price": result.get("price", 0),
            "category": result.get("category", ""),
            "description": result.get("description", ""),
            "short_description": result.get("shortDescription", ""),
            "stock": result.get("stock", 0),
            "images": result.get("images", []),
            "specifications": result.get("specifications", {}),
            "rating": result.get("rating", 0),
            "reviews_count": result.get("reviewsCount", 0)
        }
        
        return product
        
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        return {"sku": sku, "error": "Product not found"}
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"sku": sku, "error": str(e)}

async def get_all_products(limit: int = 20) -> List[Dict]:
    """
    Lấy danh sách tất cả sản phẩm.
    
    Args:
        limit: Số lượng sản phẩm tối đa
        
    Returns:
        List sản phẩm
    """
    try:
        url = settings.get_product_url()
        print(f"📊 [TOOL] get_all_products called")
        print(f"   URL: {url}")
        print(f"   Limit: {limit}")
        
        response = await http_client.get(url, params={"limit": limit})
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        items = result.get("items", []) if isinstance(result, dict) else result
        print(f"   📦 Items count: {len(items)}")
        
        formatted_items = []
        for item in items:
            formatted_items.append({
                "sku": item.get("sku", "N/A"),
                "name": item.get("name", "N/A"),
                "price": item.get("price", 0),
                "category": item.get("category", ""),
                "description": item.get("shortDescription", "")[:100],
                "stock": item.get("stock", 0)
            })
            
        print(f"   📋 Formatted {len(formatted_items)} items")
        return formatted_items
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

async def get_categories() -> List[Dict]:
    """
    Lấy danh sách danh mục sản phẩm từ Store API.
    
    Returns:
        List các danh mục
    """
    try:
        url = settings.get_category_url()
        print(f"📁 [TOOL] get_categories called")
        print(f"   URL: {url}")
        
        response = await http_client.get(url)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        categories = result if isinstance(result, list) else result.get("items", [])
        formatted = [
            {
                "id": cat.get("id", ""),
                "name": cat.get("name", "N/A"),
                "description": cat.get("description", ""),
                "product_count": cat.get("productCount", 0)
            } 
            for cat in categories
        ]
        
        print(f"   📋 Categories count: {len(formatted)}")
        return formatted
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

async def get_promotions() -> List[Dict]:
    """
    Lấy danh sách khuyến mãi từ Store API.
    
    Returns:
        List các chương trình khuyến mãi
    """
    try:
        url = settings.get_promotion_url()
        print(f"🎁 [TOOL] get_promotions called")
        print(f"   URL: {url}")
        
        response = await http_client.get(url)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        promotions = result if isinstance(result, list) else result.get("items", [])
        formatted = [
            {
                "id": promo.get("id", ""),
                "name": promo.get("name", "N/A"),
                "description": promo.get("description", ""),
                "discount": promo.get("discount", 0),
                "start_date": promo.get("startDate", ""),
                "end_date": promo.get("endDate", ""),
                "applicable_products": promo.get("applicableProducts", [])
            } 
            for promo in promotions
        ]
        
        print(f"   🎁 Promotions count: {len(formatted)}")
        return formatted
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []

async def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Kiểm tra trạng thái đơn hàng từ Store API.
    
    Args:
        order_id: Mã đơn hàng
        
    Returns:
        Dict với thông tin đơn hàng
    """
    try:
        url = settings.get_order_url(order_id)
        print(f"📋 [TOOL] get_order_status called")
        print(f"   URL: {url}")
        print(f"   Order ID: {order_id}")
        
        response = await http_client.get(url)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Response: {response.status_code}")
        
        # Format order info
        order = {
            "order_id": result.get("orderId", order_id),
            "status": result.get("status", "Unknown"),
            "created_at": result.get("createdAt", ""),
            "total_amount": result.get("totalAmount", 0),
            "items": result.get("items", []),
            "shipping_address": result.get("shippingAddress", {}),
            "tracking_number": result.get("trackingNumber", ""),
            "estimated_delivery": result.get("estimatedDelivery", "")
        }
        
        return order
        
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        return {
            "order_id": order_id,
            "error": f"Order not found: {e.response.status_code}"
        }
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {
            "order_id": order_id,
            "error": str(e)
        }

async def create_order(
    customer_id: str,
    items: List[Dict[str, Any]],
    shipping_address: Dict[str, str]
) -> Dict[str, Any]:
    """
    Tạo đơn hàng mới.
    
    Args:
        customer_id: ID khách hàng
        items: List sản phẩm [{sku, quantity}]
        shipping_address: Địa chỉ giao hàng
        
    Returns:
        Dict với thông tin đơn hàng mới
    """
    try:
        url = settings.get_order_url()
        print(f"📝 [TOOL] create_order called")
        print(f"   URL: {url}")
        
        payload = {
            "customerId": customer_id,
            "items": items,
            "shippingAddress": shipping_address
        }
        
        response = await http_client.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(f"   ✅ Order created: {result.get('orderId')}")
        return result
        
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        return {"error": f"Failed to create order: {e.response.status_code}"}
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {"error": str(e)}
