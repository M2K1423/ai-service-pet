"""Base Agent class."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from shared.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Base class cho tất cả AI agents."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize base agent.
        
        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.logger = get_logger(f"{__name__}.{name}")
    
    @abstractmethod
    async def generate_response(
        self,
        message: str,
        context: Dict[str, Any],
        history: List[Dict[str, str]]
    ) -> str:
        """
        Generate response to user message.
        
        Args:
            message: User message
            context: Context information
            history: Conversation history
        
        Returns:
            AI-generated response
        """
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Get system prompt for this agent.
        
        Returns:
            System prompt string
        """
        pass
    
    async def _call_llm(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Call LLM API to generate response.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
        
        Returns:
            LLM response
        """
        import os
        from core.config.settings import get_settings
        
        settings = get_settings()
        # Get model type (e.g. gemini, openai, claude, ollama)
        model_type = os.getenv("DEFAULT_AI_MODEL", settings.DEFAULT_AI_MODEL).lower()
        
        self.logger.info("=" * 80)
        self.logger.info(f"🤖 GỌI AI MODEL: {model_type.upper()}")
        self.logger.info("=" * 80)
        
        try:
            if model_type == "gemini":
                from integrations.ai_models.gemini_client import GeminiClient
                gemini_client = GeminiClient()
                response = await gemini_client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt
                )
                
                self.logger.info("=" * 80)
                self.logger.info(f"✅ AI MODEL GEMINI ĐÃ TRẢ LỜI")
                self.logger.info(f"📝 Response length: {len(response)} ký tự")
                self.logger.info("=" * 80)
                return response
                
            elif model_type == "openai":
                from integrations.ai_models.openai_client import OpenAIClient
                openai_client = OpenAIClient()
                response = await openai_client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt
                )
                
                self.logger.info("=" * 80)
                self.logger.info(f"✅ AI MODEL OPENAI ĐÃ TRẢ LỜI")
                self.logger.info(f"📝 Response length: {len(response)} ký tự")
                self.logger.info("=" * 80)
                return response
                
            elif model_type == "claude":
                from integrations.ai_models.claude_client import ClaudeClient
                claude_client = ClaudeClient()
                response = await claude_client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt
                )
                
                self.logger.info("=" * 80)
                self.logger.info(f"✅ AI MODEL CLAUDE ĐÃ TRẢ LỜI")
                self.logger.info(f"📝 Response length: {len(response)} ký tự")
                self.logger.info("=" * 80)
                return response
                
            else: # ollama
                from integrations.ai_models.ollama_client import OllamaClient
                model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
                ollama_client = OllamaClient(model=model_name)
                
                response = await ollama_client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt
                )
                await ollama_client.close()
                
                self.logger.info("=" * 80)
                self.logger.info(f"✅ AI MODEL OLLAMA ({model_name.upper()}) ĐÃ TRẢ LỜI")
                self.logger.info(f"📝 Response length: {len(response)} ký tự")
                self.logger.info("=" * 80)
                return response
                
        except Exception as e:
            self.logger.error(f"❌ LỖI GỌI AI MODEL {model_type.upper()}: {e}")
            return f"Xin lỗi, tôi đang gặp sự cố kỹ thuật. Vui lòng thử lại sau."

    
    def format_context(self, context: Dict[str, Any]) -> str:
        """
        Format context for LLM prompt.
        
        Args:
            context: Context dictionary
        
        Returns:
            Formatted context string
        """
        parts = []
        
        if context.get("customer_name"):
            parts.append(f"Tên khách hàng: {context['customer_name']}")
        
        if context.get("phone"):
            parts.append(f"SĐT: {context['phone']}")
        
        if context.get("email"):
            parts.append(f"Email: {context['email']}")
        
        return "\n".join(parts) if parts else "Không có thông tin khách hàng."
    
    def format_history(self, history: List[Dict[str, str]]) -> str:
        """
        Format conversation history for LLM prompt.
        
        Args:
            history: List of conversation messages
        
        Returns:
            Formatted history string
        """
        if not history:
            return "Không có lịch sử trò chuyện."
        
        formatted = []
        for msg in history[-5:]:  # Last 5 messages
            role = "Khách hàng" if msg["role"] == "user" else "AI"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
