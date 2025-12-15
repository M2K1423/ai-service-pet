"""Message processor."""
from typing import Dict, Any

from shared.logger import get_logger

logger = get_logger(__name__)


class MessageProcessor:
    """Process and normalize messages."""
    
    async def process(self, message: str) -> Dict[str, Any]:
        """
        Process incoming message.
        
        Args:
            message: Raw message
        
        Returns:
            Processed message data
        """
        # Clean and normalize message
        cleaned = self._clean_message(message)
        
        # Extract entities (TODO: implement NER)
        entities = self._extract_entities(cleaned)
        
        return {
            "original": message,
            "cleaned": cleaned,
            "entities": entities
        }
    
    def _clean_message(self, message: str) -> str:
        """Clean and normalize message."""
        # Remove extra whitespace
        cleaned = " ".join(message.split())
        
        # Convert to lowercase for processing
        # (keep original for display)
        
        return cleaned.strip()
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities from message."""
        # TODO: Implement NER (Named Entity Recognition)
        # For now, return empty dict
        return {}
