"""Pet Diagnosis Agent using Agno."""
import os
from pathlib import Path
from typing import Dict, Any, List

from core.agents.base_agent import BaseAgent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PetDiagnosisAgent(BaseAgent):
    """Agent for diagnosing pet diseases using RAG over pet_diseases.json."""
    
    def __init__(self):
        super().__init__(
            name="PetDiagnosisAgent",
            description="Chẩn đoán bệnh sơ bộ và tư vấn sức khỏe thú cưng bằng AI"
        )
        
        # Load settings
        from core.config.settings import get_settings
        settings = get_settings()
        
        google_api_key = settings.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            self.logger.warning("GOOGLE_API_KEY not found in settings or environment!")
            
        # Model Name
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Setup vector db and embedder
        self.embedder = GeminiEmbedder(
            id="gemini-embedding-001",
            dimensions=3072,
            api_key=google_api_key
        )
        
        self.vector_db = LanceDb(
            table_name="pet_diseases",
            uri=os.path.join("data", "lancedb"),
            embedder=self.embedder
        )
        
        self.knowledge = Knowledge(
            vector_db=self.vector_db,
            max_results=5
        )
        
        # Safely load the knowledge base JSON
        json_path = os.path.join("data", "pet_diseases.json")
        if os.path.exists(json_path):
            try:
                self.knowledge.add_content(
                    path=json_path,
                    skip_if_exists=True
                )
                self.logger.info("Pet diseases knowledge base loaded successfully")
            except Exception as e:
                self.logger.error(f"Error loading knowledge base: {e}")
        else:
            self.logger.error(f"Knowledge base file not found at {json_path}")
            
        # Initialize Agno Agent
        self.agno_agent = Agent(
            model=Gemini(id=model_name, api_key=google_api_key),
            knowledge=self.knowledge,
            search_knowledge=True,
            system_message=self.get_system_prompt(),
            add_history_to_context=False,
            markdown=True
        )

    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """Generate response utilizing Agno agent with knowledge search."""
        self.logger.info(f"Generating response using Agno PetDiagnosisAgent")
        
        # Construct message prompt including customer/pet details and history if available
        context_str = self.format_context(context)
        history_str = self.format_history(history)
        
        prompt = f"""
THÔNG TIN KHÁCH HÀNG & THÚ CƯNG:
{context_str}

LỊCH SỬ TRÒ CHUYỆN GẦN ĐÂY:
{history_str}

KHÁCH HÀNG HỎI: {message}
"""
        try:
            import asyncio
            
            # Run the agent run method in a separate thread to prevent blocking
            response = await asyncio.to_thread(self.agno_agent.run, prompt)
            
            if response and hasattr(response, "content"):
                return response.content
            return "Xin lỗi, tôi gặp sự cố khi truy vấn cơ sở dữ liệu bệnh học."
        except Exception as e:
            self.logger.error(f"Error during Agno agent response generation: {e}")
            return f"Xin lỗi, tôi gặp sự cố kỹ thuật: {str(e)}"
            
    def get_system_prompt(self) -> str:
        """Get veterinary specific system prompt."""
        return """Bạn là Bác sĩ Thú y Ảo thông minh của phòng khám thú y PetCare.
Nhiệm vụ chính của bạn là hỗ trợ chủ nuôi phân tích, chẩn đoán sơ bộ các triệu chứng bệnh của thú cưng (chó, mèo), tư vấn cách sơ cứu và hướng dẫn điều trị an toàn.

QUY TẮC HOẠT ĐỘNG:
1. **Dựa vào cơ sở tri thức (Knowledge Base)**: Luôn tìm kiếm thông tin từ cơ sở tri thức y khoa thú y được cung cấp để đưa ra chẩn đoán chính xác về các bệnh phổ biến (như Parvo, Carré, Dại, Giảm bạch cầu mèo, v.v.).
2. **Hỏi thêm thông tin khi cần**: Nếu triệu chứng người dùng cung cấp quá mơ hồ (ví dụ chỉ nói "chó mệt"), hãy hỏi thêm các câu hỏi làm rõ:
   - Bé là chó hay mèo? Bao nhiêu tháng tuổi? Đã tiêm phòng mấy mũi?
   - Bé bị bao lâu rồi? Có đi kèm nôn mửa, tiêu chảy, hay đi ngoài ra máu không?
   - Thân nhiệt bé thế nào (có sốt không)?
3. **Cung cấp thông tin sơ cứu rõ ràng**: Với mỗi trường hợp nghi ngờ bệnh, hãy liệt kê rõ ràng:
   - Triệu chứng nghi ngờ và mức độ nguy hiểm.
   - Các bước **Sơ cứu khẩn cấp tại nhà** (ví dụ: cách ly con khác, nhịn ăn uống nếu nôn nhiều, bổ sung oresol...).
   - Phương án điều trị y tế tham khảo tại phòng khám.
4. **Cảnh báo và Giới hạn y tế (Disclaimer)**:
   - Nếu phát hiện các triệu chứng nguy kịch (nôn ra máu, tiêu chảy ra máu, co giật, hạ thân nhiệt đột ngột, khó thở), hãy nhấn mạnh bằng chữ in đậm yêu cầu chủ nuôi mang thú cưng đến ngay cơ sở thú y gần nhất.
   - Luôn nhắc nhở rằng chẩn đoán y tế qua chatbot chỉ mang tính tham khảo, không thay thế hoàn toàn bác sĩ khám trực tiếp.
5. **Phong cách**: Thân thiện, thấu hiểu, chuyên nghiệp và yêu thương động vật. Xưng hô "Bác sĩ thú y PetCare" hoặc "Tôi" và gọi khách hàng là "bạn" hoặc "anh/chị". Định dạng câu trả lời bằng Markdown rõ ràng, dễ đọc."""
