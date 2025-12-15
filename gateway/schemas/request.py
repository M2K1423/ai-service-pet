"""Request schemas for API endpoints."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    """Schema for chat request."""
    
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., min_length=1, description="User message")
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context (customer info, history, etc.)"
    )
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "message": "Tôi muốn tư vấn sản phẩm",
                "context": {
                    "customer_name": "Nguyễn Văn A",
                    "phone": "0901234567"
                },
                "session_id": "session_abc"
            }
        }


class WebhookRequest(BaseModel):
    """Schema for webhook request."""
    
    source: str = Field(..., description="Webhook source (zalo, facebook, etc.)")
    event_type: str = Field(..., description="Event type")
    payload: Dict[str, Any] = Field(..., description="Webhook payload")
    timestamp: Optional[str] = Field(None, description="Event timestamp")
