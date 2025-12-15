"""Technical Support Agent."""
from typing import Dict, Any, List

from core.agents.base_agent import BaseAgent


class TechnicalSupportAgent(BaseAgent):
    """Agent for technical support."""
    
    def __init__(self):
        super().__init__(
            name="TechnicalSupportAgent",
            description="Handles technical support issues"
        )
    
    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Generate technical support response."""
        self.logger.info(f"Generating technical support response")
        
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
        
        response = await self._call_llm(prompt, system_prompt)
        
        return response
    
    def get_system_prompt(self) -> str:
        """Get system prompt for technical support."""
        return """Bạn là một chuyên viên hỗ trợ kỹ thuật chuyên nghiệp.

NHIỆM VỤ:
- Hỗ trợ khách hàng về vấn đề kỹ thuật
- Hướng dẫn sử dụng sản phẩm, dịch vụ
- Khắc phục sự cố, lỗi

KỸ NĂNG:
- Phân tích và chẩn đoán vấn đề
- Hướng dẫn chi tiết, từng bước
- Kiên nhẫn với khách hàng không rành kỹ thuật

PHONG CÁCH:
- Rõ ràng, dễ hiểu
- Kiên nhẫn, thấu hiểu
- Giải thích bằng ngôn ngữ đơn giản

QUY TẮC:
- Luôn xưng "em" và gọi khách hàng là "anh/chị"
- Tránh thuật ngữ kỹ thuật phức tạp
- Đưa ra hướng dẫn cụ thể, có thể thực hiện"""
