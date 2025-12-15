"""Conversation memory."""
from typing import List, Dict, Any
from collections import defaultdict

from shared.logger import get_logger

logger = get_logger(__name__)


class ConversationMemory:
    """Store and retrieve conversation history."""
    
    def __init__(self, max_messages: int = 50):
        """
        Initialize conversation memory.
        
        Args:
            max_messages: Maximum messages to keep per conversation
        """
        self.max_messages = max_messages
        self.conversations: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    
    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Add message to conversation.
        
        Args:
            conversation_id: Conversation identifier
            role: Message role (user/assistant)
            content: Message content
        """
        self.conversations[conversation_id].append({
            "role": role,
            "content": content
        })
        
        # Keep only last N messages
        if len(self.conversations[conversation_id]) > self.max_messages:
            self.conversations[conversation_id] = \
                self.conversations[conversation_id][-self.max_messages:]
    
    def get_history(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Get conversation history.
        
        Args:
            conversation_id: Conversation identifier
            limit: Maximum messages to return
        
        Returns:
            List of messages
        """
        messages = self.conversations.get(conversation_id, [])
        return messages[-limit:] if messages else []
    
    def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear conversation history.
        
        Args:
            conversation_id: Conversation identifier
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
