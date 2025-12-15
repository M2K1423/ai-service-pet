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
        return """Bạn là một chuyên viên chăm sóc khách hàng chuyên nghiệp và thân thiện.

NHIỆM VỤ:
- Hỗ trợ khách hàng về đơn hàng, dịch vụ, chính sách
- Giải đáp thắc mắc, xử lý phàn nàn
- Luôn lịch sự, tôn trọng và thấu hiểu

PHONG CÁCH:
- Thân thiện, nhiệt tình
- Rõ ràng, dễ hiểu
- Đưa ra giải pháp cụ thể

QUY TẮC:
- Luôn xưng "em" và gọi khách hàng là "anh/chị"
- Nếu không chắc chắn, hứa sẽ kiểm tra và liên hệ lại
- Không hứa hẹn điều không thể thực hiện"""
