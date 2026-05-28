"""Google Gemini API client."""
from typing import List, Dict, Any, Optional
import os
from google import genai
from google.genai.types import GenerateContentConfig

from shared.logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API key
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            logger.warning("Google API key not configured")
            raise ValueError("Google API key is required")
        
        # Initialize Gemini client (v1beta API - default)
        self.client = genai.Client(
            api_key=self.api_key,
            http_options={'api_version': 'v1beta'}
        )
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate response using Gemini.
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Temperature for generation (0.0-2.0)
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated response text
        """
        try:
            logger.info(f"Generating response with Gemini model: {self.model_name}")
            
            # Prepare content
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Configure generation
            config = GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                top_p=0.95,
                top_k=40
            )
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config=config
            )
            
            # Extract text from response
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini")
                return "Xin lỗi, tôi không thể tạo câu trả lời lúc này."
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    async def generate_streaming_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Generate streaming response using Gemini.
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Temperature for generation
        
        Yields:
            Response chunks
        """
        try:
            logger.info(f"Generating streaming response with Gemini")
            
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            config = GenerateContentConfig(
                temperature=temperature,
                top_p=0.95,
                top_k=40
            )
            
            # Stream response
            async for chunk in self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=full_prompt,
                config=config
            ):
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Gemini streaming error: {str(e)}")
            raise
