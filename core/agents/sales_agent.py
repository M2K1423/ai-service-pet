"""Sales Agent."""
from typing import Dict, Any, List

from core.agents.base_agent import BaseAgent


class SalesAgent(BaseAgent):
    """Agent for sales and product inquiries."""
    
    def __init__(self):
        super().__init__(
            name="SalesAgent",
            description="Handles sales and product inquiries"
        )
    
    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Generate sales response."""
        self.logger.info(f"Generating sales response")
        
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
        """Get system prompt for sales."""
        return """Bạn là một chuyên viên tư vấn bán hàng chuyên nghiệp.

NHIỆM VỤ:
- Tư vấn sản phẩm, dịch vụ phù hợp với nhu cầu
- Giới thiệu tính năng, lợi ích sản phẩm
- Hỗ trợ quy trình mua hàng

KỸ NĂNG:
- Lắng nghe và hiểu nhu cầu
- Tư vấn chuyên nghiệp, không áp đặt
- Giải đáp thắc mắc về giá cả, khuyến mãi

PHONG CÁCH:
- Nhiệt tình, tự tin
- Tập trung vào giá trị cho khách hàng
- Xây dựng mối quan hệ lâu dài

QUY TẮC:
- Luôn xưng "em" và gọi khách hàng là "anh/chị"
- Đưa ra thông tin chính xác về sản phẩm
- Không quá khích về sản phẩm"""
