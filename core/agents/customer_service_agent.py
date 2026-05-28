"""Customer Service Agent."""
from typing import Dict, Any, List

from core.agents.base_agent import BaseAgent


class CustomerServiceAgent(BaseAgent):
    """Agent for customer service inquiries."""
    
    def __init__(self):
        super().__init__(
            name="CustomerServiceAgent",
            description="Handles general customer service inquiries"
        )
    
    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Generate customer service response."""
        self.logger.info(f"Generating customer service response")
        
        system_prompt = self.get_system_prompt()
        context_str = self.format_context(context)
        history_str = self.format_history(history)
        
        prompt = f"""
{system_prompt}

THÔNG TIN KHÁCH HÀNG:
{context_str}

LỊCH SỬ TRÒ CHUYỆN:
{history_str}

KHÁCH HÀNG: {message}

AI:"""
        
        # Call LLM through integrations layer
        response = await self._call_llm(prompt, system_prompt)
        
        return response
    
    def get_system_prompt(self) -> str:
        """Get system prompt for customer service."""
        return """Bạn là một trợ lý thú y ảo thông minh của phòng khám PetCare.

NHIỆM VỤ:
- Tư vấn về sức khỏe thú cưng, lịch tiêm phòng, dịch vụ khám chữa bệnh
- Hỗ trợ khách hàng đặt lịch hẹn (gọi API nếu cần)
- Giải đáp thắc mắc về các sản phẩm/thuốc thú y đang bán
- Luôn lịch sự, tôn trọng và yêu thương động vật

PHONG CÁCH:
- Thân thiện, chuyên nghiệp, nhiệt tình
- Tư vấn rõ ràng, khoa học nhưng dễ hiểu
- Khuyên khách hàng mang thú cưng đến phòng khám nếu có triệu chứng nặng

QUY TẮC:
- Luôn xưng "phòng khám" hoặc "trợ lý AI" và gọi khách là "bạn" hoặc "anh/chị"
- Nếu không biết, hãy khuyên khách hàng đặt lịch khám để bác sĩ thú y tư vấn
- Không tự ý kê đơn thuốc mạnh hoặc chẩn đoán chắc chắn 100% bệnh mà không khám"""
