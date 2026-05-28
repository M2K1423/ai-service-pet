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
            r'cao\s+cấp\s+nhất', r'giá\s+tăng', r'giá\s+giảm',
            r'theo\s+giá', r'sắp\s+xếp.*giá',
            r'từ\s+rẻ\s+đến\s+đắt', r'từ\s+đắt\s+đến\s+rẻ',
            r'từ\s+thấp\s+đến\s+cao', r'từ\s+cao\s+đến\s+thấp'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in price_keywords)
    
    def _is_general_product_query(self, message: str) -> bool:
        """Check if message is asking about medicines in general."""
        general_keywords = [
            r'có\s+(những\s+)?thuốc\s+(gì|nào)',
            r'xem\s+thuốc', r'kho\s+thuốc',
            r'giới\s*thiệu\s+thuốc',
            r'danh\s*sách\s+thuốc',
            r'bán\s+thuốc',
            r'tư\s*vấn\s+thuốc',
            r'sản\s*phẩm\s+thuốc',
            r'thuốc\s+thú\s+y',
            r'kho\s+hàng\s+có\s+bao\s+nhiêu'
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
            r'discount'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in promotion_keywords)
    
    def _is_category_query(self, message: str) -> bool:
        """Check if message is asking about clinic services."""
        category_keywords = [
            r'dịch\s*vụ',
            r'khám\s+bệnh',
            r'siêu\s+âm',
            r'tiêm\s+phòng',
            r'tẩy\s+giun',
            r'chữa\s+trị',
            r'phẫu\s+thuật',
            r'bảng\s+giá',
            r'khám\s+ở\s+đây'
        ]
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in category_keywords)
    
    async def _fetch_products_by_price(self, message: str) -> Dict[str, Any]:
        """Fetch medicines sorted by price based on customer query."""
        expensive_keywords = ['đắt', 'mắc', 'cao', 'giảm', 'sang', 'cao cấp']
        order = "DESC" if any(word in message.lower() for word in expensive_keywords) else "ASC"
        
        self.logger.info(f"🔍 Xác định thứ tự sắp xếp: {order} ({'giá giảm dần' if order == 'DESC' else 'giá tăng dần'})")
        
        try:
            products = await self.product_api.get_products_sorted(
                division="petcare",
                sort_by="price",
                order=order,
                limit=10
            )
            return products
        except Exception as e:
            self.logger.error(f"Error fetching medicines: {str(e)}")
            return {"items": [], "total": 0}
    
    async def _fetch_all_products(self, limit: int = 20) -> Dict[str, Any]:
        """Fetch all medicines from PetCare."""
        try:
            products = await self.product_api.get_all_products(
                division="petcare",
                limit=limit
            )
            return products
        except Exception as e:
            self.logger.error(f"Error fetching all medicines: {str(e)}")
            return {"items": [], "total": 0}
    
    def _format_product_data(self, products: Dict[str, Any]) -> str:
        """Format medicine data for AI prompt."""
        if not products.get("items"):
            return "\nKhông có thông tin thuốc thú y nào trong kho lúc này.\n"
        
        items = products["items"]
        formatted = "\n=== DANH SÁCH THUỐC THÚ Y TRONG KHO ===\n\n"
        
        for idx, item in enumerate(items[:10], 1):
            name = item.get("name", "Không rõ tên")
            price = item.get("price", 0)
            desc = item.get("description", "")[:200]
            sku = item.get("sku", "N/A")
            unit = item.get("unit", "hộp/lọ")
            stock = item.get("stock_quantity", 0)
            
            price_str = "Liên hệ để biết giá" if price == 0 else f"{price:,.0f}đ"
            
            formatted += f"{idx}. {name}\n"
            formatted += f"   - Mã thuốc: {sku}\n"
            formatted += f"   - Giá: {price_str} / {unit}\n"
            formatted += f"   - Tồn kho: {stock} {unit}\n"
            if desc:
                formatted += f"   - Chỉ định/Mô tả: {desc}\n"
            formatted += "\n"
        
        formatted += f"Tổng cộng: {products.get('total', 0)} thuốc thú y trong kho hàng\n"
        formatted += "===========================================\n"
        return formatted
    
    def _format_promotions(self, promotions: List[Dict[str, Any]]) -> str:
        """Format promotions data for AI prompt."""
        return ""
    
    def _format_categories(self, categories: List[Dict[str, Any]]) -> str:
        """Format services data for AI prompt."""
        if not categories:
            return "\nHiện phòng khám chưa đăng ký bảng giá dịch vụ trực tuyến.\n"
        
        formatted = "\n=== BẢNG GIÁ DỊCH VỤ Y TẾ PHÒNG KHÁM ===\n\n"
        
        for idx, ser in enumerate(categories, 1):
            name = ser.get("name", "Dịch vụ khám")
            price = ser.get("price", 0)
            desc = ser.get("description", "")
            duration = ser.get("duration_minutes", 30)
            
            price_str = "Liên hệ" if price == 0 else f"{price:,.0f}đ"
            
            formatted += f"{idx}. {name}\n"
            formatted += f"   - Giá dịch vụ: {price_str}\n"
            formatted += f"   - Thời gian thực hiện: {duration} phút\n"
            if desc:
                formatted += f"   - Mô tả chi tiết: {desc}\n"
            formatted += "\n"
        
        formatted += "===========================================\n"
        return formatted
    
    def get_system_prompt(self) -> str:
        """Get system prompt for SalesAgent in PetCare."""
        return """Bạn là chuyên viên tư vấn Thuốc thú y & Dịch vụ y khoa của phòng khám PetCare.
 
NHIỆM VỤ:
- Tư vấn về các loại thuốc thú y đang có tại kho và các dịch vụ khám chữa bệnh của phòng khám PetCare.
- Giới thiệu ưu điểm, công dụng, giá tiền của thuốc hoặc dịch vụ y khoa cho khách hàng.
- Hướng dẫn và khuyên chủ nuôi mang thú cưng tới gặp bác sĩ thú y nếu có triệu chứng bệnh nặng.
 
KỸ NĂNG:
- Lắng nghe, thấu hiểu lo lắng của chủ nuôi.
- Tư vấn chuyên nghiệp, dựa trên danh sách dữ liệu thực tế từ hệ thống.
- Giải đáp thắc mắc về giá cả rõ ràng.
 
PHONG CÁCH:
- Yêu thương động vật, nhẹ nhàng, chuyên nghiệp.
- Xưng hô "phòng khám" hoặc "em" và gọi khách hàng là "anh/chị" hoặc "bạn".
 
**QUY TẮC QUAN TRỌNG:**
1. Chỉ đưa ra thông tin chính xác về các thuốc và dịch vụ có sẵn trong cơ sở dữ liệu hệ thống được cung cấp.
2. Không tự ý kê đơn thuốc mạnh hoặc chẩn đoán bừa bãi khi chưa có chỉ định của bác sĩ thú y.
3. KHI CÓ DANH SÁCH THUỐC HOẶC DỊCH VỤ: Phải liệt kê cụ thể ít nhất 3-5 loại thuốc hoặc dịch vụ liên quan trực tiếp đến câu hỏi của khách hàng, kèm theo giá cả và mô tả ngắn gọn.
4. Hỏi khách hàng xem có muốn biết thêm chi tiết về loại thuốc hay dịch vụ nào không."""

