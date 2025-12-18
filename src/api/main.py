"""
Main FastAPI Application - AI Agent System
Nhận request từ CRA Backend và xử lý qua Agno Agents
Theo sơ đồ: Zalo/Messenger -> CRA Backend -> [AI Agent] -> Store API

Flow:
1. CRA Backend nhận webhook từ Zalo/Messenger
2. CRA Backend gửi request tới AI Agent (endpoint này)
3. AI Agent sử dụng tools để gọi Store API (http://localhost:9000/odeli/...)
4. AI Agent trả kết quả về cho CRA Backend
5. CRA Backend reply lại user qua Zalo/Messenger
"""
import os
import re
from typing import Dict, Any
from agno.os import AgentOS
from fastapi import HTTPException, Header, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.agents import sales_agent
from src.core.models import ChatRequest, ChatResponse, ErrorResponse, WebhookMessage
from src.config.settings import settings

# ============================================
# AGENT OS SETUP
# ============================================

agent_os = AgentOS(
    agents=[sales_agent]
)

app = agent_os.get_app()

# ============================================
# CORS MIDDLEWARE (cho CRA Backend gọi được)
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên specify CRA Backend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# API KEY VALIDATION
# ============================================

API_KEYS = settings.API_KEYS

def validate_api_key(x_api_key: str = Header(...)):
    """Validate API key từ CRA Backend."""
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# ============================================
# ENDPOINTS
# ============================================

@app.post("/api/v1/chat", response_model=ChatResponse)
async def smart_chat(
    request: ChatRequest,
    api_key: str = Header(..., alias="X-API-Key")
):
    """
    Main chat endpoint cho CRA Backend.
    CRA Backend gửi message từ Zalo/Messenger vào đây.
    AI Agent xử lý và gọi Store API thông qua tools.
    
    Flow:
    1. Nhận message từ CRA Backend
    2. Route tới agent phù hợp (customer service/sales/tech support)
    3. Agent sử dụng tools để gọi Store API
    4. Trả kết quả về CRA Backend
    """
    
    # Validate API key từ CRA Backend
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key from CRA Backend")
    
    try:
        print("=" * 80)
        print(f"📨 [REQUEST] User: {request.user_id}")
        print(f"💬 [MESSAGE] {request.message}")
        
        # Use sales_agent for all requests
        agent = sales_agent
        print(f"🤖 [AGENT] {agent.name}")
        print(f"🔧 [TOOLS] {len(agent.tools)} tools available")
        
        # Run agent (async vì tools gọi Store API là async)
        print(f"⚙️ [PROCESSING] Running agent...")
        response = await agent.arun(request.message)
        
        # Clean response - remove JSON/code blocks
        response_text = response.content
        
        # Remove code blocks
        response_text = re.sub(r'```(?:json)?\s*\{[^`]*\}\s*```', '', response_text, flags=re.DOTALL)
        response_text = re.sub(r'```(?:json)?.*?```', '', response_text, flags=re.DOTALL)
        
        # Remove JSON objects
        response_text = re.sub(r'\{\s*"(?:name|parameters|limit|order|query|sort_by)"[^}]+\}', '', response_text, flags=re.DOTALL)
        
        # Remove tool call explanations
        if "Lưu ý:" in response_text:
            parts = response_text.split("Lưu ý:", 1)
            if len(parts) > 1:
                response_text = parts[1].strip()
        
        # Clean whitespace
        response_text = "\n".join([line.strip() for line in response_text.split("\n") if line.strip()])
        response_text = response_text.strip()
        
        # Fallback if empty
        if not response_text or len(response_text) < 10:
            response_text = response.content
        
        # Map agent type
        agent_type_map = {
            "Customer Service Agent": "customer_service",
            "Sales Agent": "sales",
            "Technical Support Agent": "technical_support",
        }
        
        print(f"✅ [RESPONSE] Length: {len(response_text)} chars")
        print(f"📤 [SENDING] Back to CRA Backend")
        print("=" * 80)
        
        return ChatResponse(
            user_id=request.user_id,
            message=response_text,
            agent_used=agent.name,
            agent_type=agent_type_map.get(agent.name, "general"),
            session_id=request.session_id or None
        )
        
    except Exception as e:
        print(f"❌ [ERROR] {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/webhook", response_model=ChatResponse)
async def webhook_handler(
    webhook: WebhookMessage,
    api_key: str = Header(..., alias="X-API-Key")
):
    """
    Webhook endpoint để nhận message trực tiếp từ platforms.
    Alternative endpoint nếu CRA Backend muốn forward raw webhook.
    """
    
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    try:
        # Convert webhook to chat request
        chat_request = ChatRequest(
            user_id=f"{webhook.platform}:{webhook.user_id}",
            message=webhook.message,
            session_id="",
            context={"platform": webhook.platform, "timestamp": webhook.timestamp}
        )
        
        # Reuse smart_chat logic
        return await smart_chat(chat_request, api_key)
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """
    Health check endpoint.
    CRA Backend có thể dùng để check AI Agent service còn hoạt động không.
    """
    return {
        "status": "healthy",
        "service": "Agno AI Sales Agent",
        "version": "1.0.0",
        "store_api": settings.STORE_API_BASE_URL,
        "agent": {
            "name": sales_agent.name,
            "tools": len(sales_agent.tools),
            "type": "sales"
        }
    }

@app.get("/api/v1/agents")
async def list_agents():
    """List agent và tools."""
    return {
        "agent": {
            "name": sales_agent.name,
            "type": "sales",
            "tools": [tool.__name__ for tool in sales_agent.tools],
            "description": "Tư vấn sản phẩm, tìm kiếm, giá cả, khuyến mãi"
        }
    }

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 80)
    print("🚀 AGNO AI AGENT SYSTEM - STARTING")
    print("=" * 80)
    print(f"📡 Architecture Flow:")
    print(f"   Zalo/Messenger → CRA Backend → [AI Agent] → Store API")
    print(f"")
    print(f"🔗 Store API Backend: {settings.STORE_API_BASE_URL}")
    print(f"")
    print(f"📊 API Documentation: http://localhost:8000/docs")
    print(f"🔍 Health Check: http://localhost:8000/api/v1/health")
    print(f"💬 Chat Endpoint: POST http://localhost:8000/api/v1/chat")
    print(f"📱 Webhook Endpoint: POST http://localhost:8000/api/v1/webhook")
    print(f"🤖 Agents List: GET http://localhost:8000/api/v1/agents")
    print(f"")
    print(f"🤖 AI Agent:")
    print(f"   {sales_agent.name}")
    print(f"   Tools: {', '.join([t.__name__ for t in sales_agent.tools])}")
    print(f"")
    print(f"📝 CRA Backend cần gửi request với:")
    print(f"   - Header: X-API-Key: <your-api-key>")
    print(f"   - Body: {{user_id, message, session_id?, context?}}")
    print("=" * 80)
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
