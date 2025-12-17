"""Sales Agent."""
from typing import Dict, Any, List
import os
import re

from core.agents.base_agent import BaseAgent
from integrations.database_api.client import DatabaseAPIClient
from integrations.database_api.products import ProductAPI


class SalesAgent(BaseAgent):
    """Agent for sales and product inquiries."""
    
    def __init__(self):
        super().__init__(
            name="SalesAgent",
            description="Handles sales and product inquiries"
        )
        
        # Initialize database API client
        api_url = os.getenv("DATABASE_API_URL", "http://localhost:9000")
        api_key = os.getenv("DATABASE_API_KEY", "")
        self.db_client = DatabaseAPIClient(api_url, api_key)
        self.product_api = ProductAPI(self.db_client)
    
    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Generate sales response."""
        self.logger.info(f"Generating sales response")
        
        # Detect query type and fetch data accordingly
        product_data = ""
        if self._is_price_query(message):
            self.logger.info("🔍 Phát hiện câu hỏi về giá sản phẩm, gọi API...")
            products = await self._fetch_products_by_price(message)
            if products and products.get("items"):
                product_data = self._format_product_data(products)
                self.logger.info(f"📦 Có {len(products['items'])} sản phẩm để tư vấn")
        elif self._is_promotion_query(message):
            self.logger.info("🎁 Phát hiện câu hỏi về khuyến mãi, gọi API...")
            promotions = await self.product_api.get_promotions(division="odeli")
            if promotions:
                product_data = self._format_promotions(promotions)
                self.logger.info(f"🎁 Có {len(promotions)} khuyến mãi")
        elif self._is_category_query(message):
            self.logger.info("📁 Phát hiện câu hỏi về danh mục, gọi API...")
            categories = await self.product_api.get_categories(division="odeli")
            if categories:
                product_data = self._format_categories(categories)
                self.logger.info(f"📁 Có {len(categories)} danh mục")
        elif self._is_general_product_query(message):
            self.logger.info("🔍 Phát hiện câu hỏi chung về sản phẩm, gọi API...")
            products = await self._fetch_all_products()
            if products and products.get("items"):
                product_data = self._format_product_data(products)
                self.logger.info(f"📦 Có {len(products['items'])} sản phẩm để tư vấn")
        
        system_prompt = self.get_system_prompt()
        context_str = self.format_context(context)
        history_str = self.format_history(history)
        
        prompt = f"""
{system_prompt}

THÔNG TIN KHÁCH HÀNG:
{context_str}

LỊCH SỬ TRÒ CHUYỆN:
{history_str}

{product_data}

KHÁCH HÀNG: {message}

AI:"""
        
        response = await self._call_llm(prompt, system_prompt)
        
        return response
    
    def _is_price_query(self, message: str) -> bool:
        """Check if message is asking about products by price."""
        price_keywords = [
            r'rẻ\s+nhất', r'giá\s+rẻ', r'giá\s+thấp',
            r'đắt\s+nhất', r'giá\s+cao', r'giá\s+đắt',
            r'mắc\s+nhất', r'giá\s+mắc', r'đắt\s+tiền',
            r'cao\s+cấp\s+nhất', r'sang\s+trọng\s+nhất',
            r'giá\s+tăng', r'giá\s+giảm',
            r'theo\s+giá', r'sắp\s+xếp.*giá',
            r'từ\s+rẻ\s+đến\s+đắt', r'từ\s+đắt\s+đến\s+rẻ',
            r'từ\s+thấp\s+đến\s+cao', r'từ\s+cao\s+đến\s+thấp'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in price_keywords)
    
    def _is_general_product_query(self, message: str) -> bool:
        """Check if message is asking about products in general."""
        general_keywords = [
            r'có\s+(những\s+)?sản\s*phẩm\s+(gì|nào)',
            r'xem\s+sản\s*phẩm',
            r'giới\s*thiệu\s+(sản\s*phẩm|món)',
            r'menu',
            r'danh\s*sách\s+(sản\s*phẩm|món)',
            r'bán\s+(gì|những\s+gì)',
            r'có\s+(món|thức\s+ăn)\s+(gì|nào)',
            r'tư\s*vấn\s+sản\s*phẩm',
            r'sản\s*phẩm\s+nào',
            r'món\s+ăn\s+(gì|nào)'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in general_keywords)
    
    def _is_promotion_query(self, message: str) -> bool:
        """Check if message is asking about promotions."""
        promotion_keywords = [
            r'khuyến\s*mãi',
            r'giảm\s*giá',
            r'ưu\s*đãi',
            r'combo',
            r'khuyến\s*mại',
            r'sale',
            r'discount',
            r'chương\s*trình'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in promotion_keywords)
    
    def _is_category_query(self, message: str) -> bool:
        """Check if message is asking about categories."""
        category_keywords = [
            r'danh\s*mục',
            r'loại\s+(món|sản\s*phẩm)',
            r'phân\s*loại',
            r'category',
            r'categories',
            r'nhóm\s+(sản\s*phẩm|món)'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in category_keywords)
    
    async def _fetch_products_by_price(self, message: str) -> Dict[str, Any]:
        """Fetch products sorted by price based on customer query."""
        # Determine sort order (ASC or DESC)
        # DESC: expensive first (đắt, mắc, cao, giảm dần)
        # ASC: cheap first (rẻ, thấp, tăng dần)
        expensive_keywords = ['đắt', 'mắc', 'cao', 'giảm', 'sang', 'cao cấp']
        order = "DESC" if any(word in message.lower() for word in expensive_keywords) else "ASC"
        
        self.logger.info(f"🔍 Xác định thứ tự sắp xếp: {order} ({'giá giảm dần' if order == 'DESC' else 'giá tăng dần'})")
        
        try:
            products = await self.product_api.get_products_sorted(
                division="odeli",
                sort_by="price",
                order=order,
                limit=10
            )
            return products
        except Exception as e:
            self.logger.error(f"Error fetching products: {str(e)}")
            return {"items": [], "total": 0}
    
    async def _fetch_all_products(self, limit: int = 20) -> Dict[str, Any]:
        """Fetch all products from system."""
        try:
            products = await self.product_api.get_all_products(
                division="odeli",
                limit=limit
            )
            return products
        except Exception as e:
            self.logger.error(f"Error fetching all products: {str(e)}")
            return {"items": [], "total": 0}
    
    def _format_product_data(self, products: Dict[str, Any]) -> str:
        """Format product data for AI prompt."""
        if not products.get("items"):
            return ""
        
        items = products["items"]
        formatted = "\n=== DANH SÁCH SẢN PHẨM TỮ HỆ THỐNG ===\n\n"
        
        for idx, item in enumerate(items[:10], 1):
            name = item.get("name", "Không rõ tên")
            price = item.get("price", 0)
            desc = item.get("shortDescription", item.get("description", ""))[:200]
            sku = item.get("sku", "N/A")
            
            # Xử lý giá = 0
            price_str = "Liên hệ để biết giá" if price == 0 else f"{price:,.0f}đ"
            
            formatted += f"{idx}. {name}\n"
            formatted += f"   - Mã SP: {sku}\n"
            formatted += f"   - Giá: {price_str}\n"
            if desc:
                formatted += f"   - Mô tả: {desc}\n"
            formatted += "\n"
        
        formatted += f"Tổng cộng: {products.get('total', 0)} sản phẩm trong hệ thống\n"
        formatted += "===========================================\n"
        return formatted
    
    def _format_promotions(self, promotions: List[Dict[str, Any]]) -> str:
        """Format promotions data for AI prompt."""
        if not promotions:
            return ""
        
        formatted = "\n=== DANH SÁCH KHUYẾN MÃI & COMBO ===\n\n"
        
        for idx, promo in enumerate(promotions[:10], 1):
            name = promo.get("name", "Không rõ tên")
            desc = promo.get("description", "")[:200]
            discount = promo.get("discount", 0)
            
            formatted += f"{idx}. {name}\n"
            if discount:
                formatted += f"   - Giảm giá: {discount}%\n"
            if desc:
                formatted += f"   - Mô tả: {desc}\n"
            formatted += "\n"
        
        formatted += "===========================================\n"
        return formatted
    
    def _format_categories(self, categories: List[Dict[str, Any]]) -> str:
        """Format categories data for AI prompt."""
        if not categories:
            return ""
        
        formatted = "\n=== DANH MỤC SẢN PHẨM ===\n\n"
        
        for idx, cat in enumerate(categories, 1):
            name = cat.get("name", "Không rõ tên")
            desc = cat.get("description", "")
            
            formatted += f"{idx}. {name}\n"
            if desc:
                formatted += f"   - Mô tả: {desc}\n"
        
        formatted += "\n===========================================\n"
        return formatted
    
    def get_system_prompt(self) -> str:
        """Get system prompt for sales."""
        return """Bạn là một chuyên viên tư vấn bán hàng chuyên nghiệp.

NHIỆM VỤ:
- Tư vấn sản phẩm, dịch vụ phù hợp với nhu cầu
- Giới thiệu tính năng, lợi ích sản phẩm
- Hỗ trợ quy trình mua hàng

KỸ NĂNG:
- Lắng nghe và hiểu nhu cầu
- Tư vấn chuyên nghiệp, không áp đặt
- Giải đáp thắc mắc về giá cả, khuyến mãi

PHONG CÁCH:
- Nhiệt tình, tự tin
- Tập trung vào giá trị cho khách hàng
- Xây dựng mối quan hệ lâu dài

**QUY TẮC QUAN TRỌNG:**
1. Luôn xưng "em" và gọi khách hàng là "anh/chị"
2. Đưa ra thông tin chính xác về sản phẩm
3. Không quá khích về sản phẩm
4. **KHI CÓ DANH SÁCH SẢN PHẨM: PHẢI LIỆT KÊ CỤ TH ít nhất 3-5 SẢN PHẨM ĐẦU TIÊN**
5. Giới thiệu ngắn gọn tên sản phẩm, giá và ưu điểm nổi bật
6. Hỏi khách hàng muốn biết thêm chi tiết sản phẩm nào"""
