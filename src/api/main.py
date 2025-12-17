"""
Main FastAPI Application
Xử lý API endpoints và khởi động service
"""
import os
import re
from typing import Dict, Any
from agno.os import AgentOS
from fastapi import HTTPException, Header
from pydantic import BaseModel
from src.core.agents import customer_service_agent, sales_agent, tech_support_agent, SimpleRouter

# ============================================
# AGENT OS SETUP
# ============================================

agent_os = AgentOS(
    agents=[customer_service_agent, sales_agent, tech_support_agent]
)

app = agent_os.get_app()

# ============================================
# API MODELS
# ============================================

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

# ============================================
# API KEY VALIDATION
# ============================================

API_KEYS = os.getenv("API_KEYS", "test-key-123,dev-key-456").split(",")

def validate_api_key(x_api_key: str = Header(...)):
    """Validate API key."""
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
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
