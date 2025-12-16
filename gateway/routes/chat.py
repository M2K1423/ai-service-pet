"""Chat endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict

from gateway.schemas.request import ChatRequest
from gateway.schemas.response import ChatResponse
from gateway.middleware.auth import verify_api_key
from core.agent_manager import AgentManager
from shared.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Handle chat messages from CRM.
    
    Args:
        request: Chat request with user message and context
        api_key: Validated API key
    
    Returns:
        ChatResponse with AI-generated reply
    """
    try:
        # ============================================
        # LOG CHI TIẾT REQUEST TỪ CRM
        # ============================================
        logger.info("=" * 80)
        logger.info("🔔 NHẬN REQUEST TỪ CRM")
        logger.info("=" * 80)
        logger.info(f"📨 User ID: {request.user_id}")
        logger.info(f"💬 Message: {request.message}")
        logger.info(f"📋 Session ID: {getattr(request, 'session_id', 'N/A')}")
        logger.info(f"🔑 API Key: {api_key[:8]}...")
        logger.info(f"📦 Context: {request.context}")
        logger.info(f"🕐 Timestamp: {request.timestamp if hasattr(request, 'timestamp') else 'N/A'}")
        logger.info("=" * 80)
        
        # Get or create agent manager
        agent_manager = AgentManager()
        
        # Process message through core layer
        logger.info("🤖 Bắt đầu xử lý với AI Agent...")
        response = await agent_manager.process_message(
            user_id=request.user_id,
            message=request.message,
            context=request.context
        )
        
        logger.info("=" * 80)
        logger.info("✅ TRẢ RESPONSE CHO CRM")
        logger.info("=" * 80)
        logger.info(f"💬 AI Response: {response.get('message', '')}")
        logger.info(f"🤖 Agent Type: {response.get('agent_type', 'general')}")
        logger.info(f"📊 Metadata: {response.get('metadata', {})}")
        logger.info("=" * 80)
        
        return ChatResponse(
            user_id=request.user_id,
            message=response.get("message", ""),
            agent_type=response.get("agent_type", "general"),
            metadata=response.get("metadata", {})
        )
        
    except Exception as e:
        logger.error("=" * 80)
        logger.error("❌ LỖI KHI XỬ LÝ REQUEST TỪ CRM")
        logger.error("=" * 80)
        logger.error(f"🚨 Error: {str(e)}")
        logger.error(f"📍 Error Type: {type(e).__name__}")
        import traceback
        logger.error(f"📋 Traceback:\n{traceback.format_exc()}")
        logger.error("=" * 80)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )
