"""
Store API Integration Tools
Tools để Agno Agent gọi tới Store Backend API
Theo sơ đồ: AI Agent -> Store API (/odeli/products/xxx)
"""
from typing import Dict, Any, List, Optional
import httpx
from src.config.settings import settings
from src.helpers.text_utils import clean_html, format_single_product, format_api_product_response

# HTTP Client với retry và timeout
http_client = httpx.AsyncClient(
    timeout=settings.HTTP_TIMEOUT,
    follow_redirects=True
)

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
                "image": item.get("thumbnailSmall", ""),
                "description": clean_html(item.get("description", "")),
                "short_description": clean_html(item.get("shortDescription", "")),
                "user_manual": clean_html(item.get("userManual", "")),
                "storage_instructions": clean_html(item.get("storageInstructions", "")),
                "category_id": item.get("categoryId", ""),
                "tags": item.get("tags", [])
            })
        
        # Display full product information using text_utils formatter
        print(f"   📋 Formatted {len(formatted_items)} items:")
        print("\n" + "=" * 100)
        for idx, product in enumerate(formatted_items, 1):
            # Use format_single_product to display ALL information
            full_info = format_single_product(product, idx)
            print(full_info)
            print("\n" + "-" * 100)
        
        return formatted_items
        
    except httpx.HTTPStatusError as e:
        print(f"   ❌ HTTP Error: {e.response.status_code}")
        return []
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return []
