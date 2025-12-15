"""Ollama local AI client."""
from typing import Optional
import httpx

from shared.logger import get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Client for local Ollama AI models."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama server URL (default: http://localhost:11434)
            model: Model name (default: llama3.2)
        """
        self.base_url = base_url
        self.model_name = model
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate response using Ollama.
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Temperature for generation (0.0-2.0)
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated response text
        """
        try:
            logger.info(f"Generating response with Ollama model: {self.model_name}")
            
            # Combine system prompt and user prompt
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Call Ollama API
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    }
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response text
            if result and "response" in result:
                return result["response"].strip()
            else:
                logger.warning("Empty response from Ollama")
                return "Xin lỗi, tôi không thể tạo câu trả lời lúc này."
            
        except httpx.HTTPError as e:
            logger.error(f"Ollama HTTP error: {str(e)}")
            raise Exception(f"Ollama connection error. Make sure Ollama is running: {str(e)}")
        except Exception as e:
            logger.error(f"Ollama API error: {str(e)}")
            raise
    
    async def generate_streaming_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Generate streaming response using Ollama.
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Temperature for generation
        
        Yields:
            Response chunks
        """
        try:
            logger.info(f"Generating streaming response with Ollama")
            
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            async with self.client.stream(
                "POST",
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                    }
                }
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        import json
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
                    
        except Exception as e:
            logger.error(f"Ollama streaming error: {str(e)}")
            raise
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
