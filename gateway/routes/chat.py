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
        logger.info(f"Chat request from user: {request.user_id}")
        
        # Get or create agent manager
        agent_manager = AgentManager()
        
        # Process message through core layer
        response = await agent_manager.process_message(
            user_id=request.user_id,
            message=request.message,
            context=request.context
        )
        
        return ChatResponse(
            user_id=request.user_id,
            message=response.get("message", ""),
            agent_type=response.get("agent_type", "general"),
            metadata=response.get("metadata", {})
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )
