"""Intent classifier."""
from typing import Dict, Any

from shared.logger import get_logger

logger = get_logger(__name__)


class IntentClassifier:
    """Classify user intent from message."""
    
    def __init__(self):
        """Initialize intent classifier."""
        self.intents = {
            "product_inquiry": ["sản phẩm", "giá", "mua", "bán", "tư vấn"],
            "order_status": ["đơn hàng", "order", "giao hàng", "vận chuyển"],
            "complaint": ["khiếu nại", "phàn nàn", "không hài lòng", "tệ"],
            "technical_issue": ["lỗi", "không hoạt động", "bug", "sự cố"],
        }
    
    async def classify(self, message: str) -> Dict[str, Any]:
        """
        Classify intent from message.
        
        Args:
            message: User message
        
        Returns:
            Dict with intent and confidence
        """
        message_lower = message.lower()
        
        # Simple keyword-based classification
        scores = {}
        for intent, keywords in self.intents.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return {
                "intent": "general",
                "confidence": 0.5
            }
        
        # Get intent with highest score
        best_intent = max(scores.items(), key=lambda x: x[1])
        
        return {
            "intent": best_intent[0],
            "confidence": min(best_intent[1] / 3.0, 1.0)  # Normalize
        }
