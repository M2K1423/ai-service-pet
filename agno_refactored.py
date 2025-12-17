from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from agno.os import AgentOS
from typing import Dict, Any, List
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CUSTOM TOOLS (thay thế integrations layer)
# ============================================

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

# ============================================
# SYSTEM PROMPTS (từ core/agents/)
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
# CREATE AGENTS (thay thế core/agents/)
# ============================================

# NOTE: Có thể thay Gemini bằng Ollama để chạy local:
# from agno.models.ollama import Ollama
# model=Ollama(id="llama3.2")

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
# AGENT ROUTER (thay thế core/processors/intent_classifier.py)
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

# ============================================
# AGENT OS (thay thế gateway/app.py)
# ============================================

agent_os = AgentOS(
    agents=[customer_service_agent, sales_agent, tech_support_agent]
)

app = agent_os.get_app()

# ============================================
# CUSTOM ENDPOINTS (thêm vào AgentOS app)
# ============================================

from fastapi import HTTPException, Header
from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str = ""
    context: Dict[str, Any] = {}

class ChatResponse(BaseModel):
    user_id: str
    message: str
    agent_used: str
    agent_type: str

# API Key validation
API_KEYS = os.getenv("API_KEYS", "test-key-123,dev-key-456").split(",")

def validate_api_key(x_api_key: str = Header(...)):
    """Validate API key."""
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.post("/api/v1/chat", response_model=ChatResponse)
async def smart_chat(
    request: ChatRequest,
    api_key: str = Header(..., alias="X-API-Key")
):
    """Smart chat với auto agent selection."""
    
    # Validate API key
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        print(f"📨 Request from user: {request.user_id}")
        print(f"💬 Message: {request.message}")
        
        # Route to appropriate agent
        agent = SimpleRouter.route(request.message)
        print(f"🤖 Routing to: {agent.name}")
        
        # Run agent (async because tools are async)
        response = await agent.arun(request.message)
        
        # Clean response - aggressively remove all JSON/code blocks
        response_text = response.content
        
        # Remove all code blocks (```json, ```, etc.)
        import re
        # Remove everything between ``` markers
        response_text = re.sub(r'```(?:json)?\s*\{[^`]*\}\s*```', '', response_text, flags=re.DOTALL)
        response_text = re.sub(r'```(?:json)?.*?```', '', response_text, flags=re.DOTALL)
        
        # Remove standalone JSON objects that might remain
        response_text = re.sub(r'\{\s*"(?:name|parameters|limit|order|query|sort_by)"[^}]+\}', '', response_text, flags=re.DOTALL)
        
        # Remove "Lưu ý:" prefix if exists (tool call explanation)
        if "Lưu ý:" in response_text:
            parts = response_text.split("Lưu ý:", 1)
            if len(parts) > 1:
                response_text = parts[1].strip()
        
        # Clean up extra whitespace
        response_text = "\n".join([line.strip() for line in response_text.split("\n") if line.strip()])
        response_text = response_text.strip()
        
        # If response is empty after cleaning, use original
        if not response_text or len(response_text) < 10:
            response_text = response.content
        
        # Determine agent type
        agent_type_map = {
            "Customer Service Agent": "customer_service",
            "Sales Agent": "sales",
            "Technical Support Agent": "technical_support",
        }
        
        return ChatResponse(
            user_id=request.user_id,
            message=response_text,
            agent_used=agent.name,
            agent_type=agent_type_map.get(agent.name, "general")
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Agno Multi-Agent System",
        "agents": [
            customer_service_agent.name,
            sales_agent.name,
            tech_support_agent.name
        ]
    }

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("🚀 Starting Agno Multi-Agent System")
    print("=" * 80)
    print(f"📊 API docs: http://localhost:8000/docs")
    print(f"🔍 Health check: http://localhost:8000/api/v1/health")
    print(f"💬 Chat endpoint: POST http://localhost:8000/api/v1/chat")
    print(f"🤖 Available agents:")
    print(f"   - {customer_service_agent.name}")
    print(f"   - {sales_agent.name}")
    print(f"   - {tech_support_agent.name}")
    print("=" * 80)
    uvicorn.run("agno_refactored:app", host="0.0.0.0", port=8000, reload=True)
