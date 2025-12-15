"""Response schemas for API endpoints."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    user_id: str = Field(..., description="User identifier")
    message: str = Field(..., description="AI-generated response")
    agent_type: str = Field(..., description="Type of agent used")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional metadata"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "message": "Chào bạn! Tôi có thể giúp bạn tư vấn sản phẩm...",
                "agent_type": "sales_agent",
                "metadata": {
                    "intent": "product_inquiry",
                    "confidence": 0.95
                },
                "timestamp": "2025-12-14T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Schema for error response."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")
    code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )
