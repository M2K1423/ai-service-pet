"""
Data Models
Pydantic models cho request/response validation
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# ============================================
# REQUEST MODELS
# ============================================

class ChatRequest(BaseModel):
    """Request model cho chat endpoint."""
    user_id: str = Field(..., description="ID của user gửi tin nhắn")
    message: str = Field(..., description="Nội dung tin nhắn")
    session_id: Optional[str] = Field("", description="Session ID để maintain context")
    context: Dict[str, Any] = Field(default_factory=dict, description="Context bổ sung")

class WebhookMessage(BaseModel):
    """Webhook message từ Zalo/Messenger."""
    platform: str = Field(..., description="Platform: zalo hoặc messenger")
    user_id: str = Field(..., description="User ID từ platform")
    message: str = Field(..., description="Nội dung tin nhắn")
    timestamp: int = Field(..., description="Timestamp của message")

# ============================================
# RESPONSE MODELS
# ============================================

class ChatResponse(BaseModel):
    """Response model cho chat endpoint."""
    user_id: str = Field(..., description="ID của user")
    message: str = Field(..., description="Câu trả lời từ agent")
    agent_used: str = Field(..., description="Tên agent đã xử lý")
    agent_type: str = Field(..., description="Loại agent")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    session_id: Optional[str] = Field(None, description="Session ID")

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Mô tả lỗi")
    detail: Optional[str] = Field(None, description="Chi tiết lỗi")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

# ============================================
# STORE API MODELS (cho internal use)
# ============================================

class Product(BaseModel):
    """Product model."""
    sku: str
    name: str
    price: float
    category: Optional[str] = None
    description: Optional[str] = None
    stock: int = 0
    image_url: Optional[str] = None

class Category(BaseModel):
    """Category model."""
    id: str
    name: str
    description: Optional[str] = None
    product_count: int = 0

class Promotion(BaseModel):
    """Promotion model."""
    id: str
    name: str
    description: str
    discount: float
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Order(BaseModel):
    """Order model."""
    order_id: str
    customer_id: str
    status: str
    total_amount: float
    created_at: str
    items: List[Dict[str, Any]] = []
    shipping_address: Dict[str, str] = {}

class Customer(BaseModel):
    """Customer model."""
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
