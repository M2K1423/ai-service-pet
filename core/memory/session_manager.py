"""Session manager."""
from typing import List, Dict, Any, Optional

from core.memory.conversation_memory import ConversationMemory
from shared.logger import get_logger

logger = get_logger(__name__)


class SessionManager:
    """Manage user sessions and conversations."""
    
    def __init__(self):
        """Initialize session manager."""
        self.memory = ConversationMemory()
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    async def get_or_create_session(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Get existing session or create new one.
        
        Args:
            user_id: User identifier
            session_id: Optional session identifier
        
        Returns:
            Session identifier
        """
        if session_id and session_id in self.sessions:
            return session_id
        
        # Create new session
        new_session_id = session_id or f"session_{user_id}_{len(self.sessions)}"
        self.sessions[new_session_id] = {
            "user_id": user_id,
            "created_at": None,  # TODO: Add timestamp
        }
        
        return new_session_id
    
    async def add_message(
        self,
        user_id: str,
        role: str,
        content: str,
        session_id: Optional[str] = None
    ) -> None:
        """
        Add message to session.
        
        Args:
            user_id: User identifier
            role: Message role
            content: Message content
            session_id: Optional session identifier
        """
        sid = await self.get_or_create_session(user_id, session_id)
        self.memory.add_message(sid, role, content)
    
    async def get_history(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        """
        Get conversation history.
        
        Args:
            user_id: User identifier
            session_id: Optional session identifier
            limit: Maximum messages to return
        
        Returns:
            List of messages
        """
        sid = await self.get_or_create_session(user_id, session_id)
        return self.memory.get_history(sid, limit)
    
    async def clear_session(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> None:
        """
        Clear session data.
        
        Args:
            user_id: User identifier
            session_id: Optional session identifier
        """
        sid = await self.get_or_create_session(user_id, session_id)
        self.memory.clear_conversation(sid)
        
        if sid in self.sessions:
            del self.sessions[sid]
