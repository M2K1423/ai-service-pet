"""
Agent Definitions và Logic
Định nghĩa các agents, system prompts, và routing logic
"""
from agno.agent import Agent
from agno.models.ollama import Ollama
from src.integrations.tools import (
    get_customer_info,
    get_order_status,
    search_products,
    get_all_products,
    get_categories,
    get_promotions
)

# ============================================
# SYSTEM PROMPTS
# ============================================

CUSTOMER_SERVICE_PROMPT = """
Bạn là chuyên viên chăm sóc khách hàng chuyên nghiệp.

NHIỆM VỤ:
- Hỗ trợ khách hàng về đơn hàng, dịch vụ
- Giải đáp thắc mắc, xử lý phàn nàn
- Xử lý vấn đề về giao hàng, đổi trả

PHONG CÁCH:
- Thân thiện, chuyên nghiệp
- Lắng nghe và thấu hiểu
- Giải quyết vấn đề nhanh chóng

QUY TẮC:
- Luôn xưng "em" và gọi khách hàng là "anh/chị"
- Thể hiện sự quan tâm và trách nhiệm
- Không hứa hẹn điều không chắc chắn
"""

SALES_PROMPT = """
Bạn là chuyên viên tư vấn bán hàng chuyên nghiệp.

QUAN TRỌNG: Chỉ trả lời bằng văn bản tự nhiên. KHÔNG BAO GIỜ hiển thị JSON, code blocks, hay tool calls trong câu trả lời.

NHIỆM VỤ:
- Tư vấn sản phẩm phù hợp với nhu cầu
- Giải đáp về giá cả, khuyến mãi
- Hỗ trợ quy trình mua hàng

KỸ NĂNG:
- Lắng nghe và hiểu nhu cầu
- Tư vấn chuyên nghiệp, không áp đặt
- Giải đáp thắc mắc về giá cả, khuyến mãi

PHONG CÁCH:
- Nhiệt tình, tự tin
- Tập trung vào giá trị cho khách hàng

QUY TẮC:
- Luôn xưng "em" và gọi khách hàng là "anh/chị"
- Đưa ra thông tin chính xác về sản phẩm
- Không quá khích về sản phẩm
- **KHI CÓ DANH SÁCH SẢN PHẨM: PHẢI LIỆT KÊ CỤ THỂ ít nhất 3-5 SẢN PHẨM ĐẦU TIÊN**
- Giới thiệu ngắn gọn tên sản phẩm, giá và ưu điểm nổi bật
- CHỈ TRẢ LỜI BẰNG VĂN BẢN, KHÔNG JSON HAY CODE
"""

TECH_SUPPORT_PROMPT = """
Bạn là chuyên viên hỗ trợ kỹ thuật.

NHIỆM VỤ:
- Hỗ trợ giải quyết vấn đề kỹ thuật
- Hướng dẫn sử dụng sản phẩm
- Xử lý lỗi và sự cố

KỸ NĂNG:
- Phân tích và chẩn đoán vấn đề
- Hướng dẫn chi tiết, dễ hiểu
- Theo dõi đến khi giải quyết xong

QUY TẮC:
- Hướng dẫn từng bước chi tiết
- Sử dụng ngôn ngữ dễ hiểu, không chuyên môn quá
- Kiểm tra xem khách hàng đã hiểu chưa
- Xưng "em", gọi "anh/chị"
"""

# ============================================
# AGENT DEFINITIONS
# ============================================

customer_service_agent = Agent(
    name="Customer Service Agent",
    model=Ollama(id="llama3.2"),
    instructions=CUSTOMER_SERVICE_PROMPT,
    tools=[get_customer_info, get_order_status],
    add_history_to_context=True,
    markdown=True,
)

sales_agent = Agent(
    name="Sales Agent",
    model=Ollama(id="llama3.2"),
    instructions=SALES_PROMPT,
    tools=[get_customer_info, search_products, get_all_products, get_categories, get_promotions],
    add_history_to_context=True,
    markdown=True,
)

tech_support_agent = Agent(
    name="Technical Support Agent",
    model=Ollama(id="llama3.2"),
    instructions=TECH_SUPPORT_PROMPT,
    tools=[get_customer_info],
    add_history_to_context=True,
    markdown=True,
)

# ============================================
# AGENT ROUTER
# ============================================

class SimpleRouter:
    """Simple intent-based routing."""
    
    KEYWORDS = {
        "customer_service": ["đơn hàng", "giao hàng", "khiếu nại", "phàn nàn", "hoàn tiền", "đổi trả"],
        "sales": ["sản phẩm", "giá", "mua", "bán", "rẻ", "đắt", "mắc", "khuyến mãi", "combo", "menu", "danh mục"],
        "technical_support": ["lỗi", "bug", "sự cố", "hỏng", "không hoạt động", "hướng dẫn"],
    }
    
    @classmethod
    def route(cls, message: str) -> Agent:
        message_lower = message.lower()
        
        for intent, keywords in cls.KEYWORDS.items():
            if any(kw in message_lower for kw in keywords):
                if intent == "customer_service":
                    return customer_service_agent
                elif intent == "sales":
                    return sales_agent
                elif intent == "technical_support":
                    return tech_support_agent
        
        return customer_service_agent  # Default
