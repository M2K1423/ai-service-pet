"""Agent Manager - Quản lý các AI agents."""
from typing import Dict, Any, Optional

from core.agents.customer_service_agent import CustomerServiceAgent
from core.agents.sales_agent import SalesAgent
from core.agents.technical_support_agent import TechnicalSupportAgent
from core.agents.pet_diagnosis_agent import PetDiagnosisAgent
from core.processors.intent_classifier import IntentClassifier
from core.processors.context_builder import ContextBuilder
from core.memory.session_manager import SessionManager
from shared.logger import get_logger

logger = get_logger(__name__)


class AgentManager:
    """Quản lý và điều phối các AI agents."""
    
    def __init__(self):
        """Initialize agent manager with available agents."""
        self.agents = {
            "customer_service": CustomerServiceAgent(),
            "sales": SalesAgent(),
            "technical_support": TechnicalSupportAgent(),
            "pet_diagnosis": PetDiagnosisAgent(),
        }
        self.intent_classifier = IntentClassifier()
        self.context_builder = ContextBuilder()
        self.session_manager = SessionManager()
    
    async def process_message(
        self,
        user_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user message and return AI response.
        
        Args:
            user_id: User identifier
            message: User message
            context: Additional context
        
        Returns:
            Dict containing response and metadata
        """
        try:
            logger.info(f"Processing message for user {user_id}")
            
            # Classify intent
            intent = await self.intent_classifier.classify(message)
            logger.info(f"Classified intent: {intent.get('intent')}")
            
            # Build context
            full_context = await self.context_builder.build(
                user_id=user_id,
                message=message,
                intent=intent,
                additional_context=context or {}
            )
            
            # Get conversation history
            history = await self.session_manager.get_history(user_id)
            
            # Select appropriate agent
            agent_type = self._select_agent(intent)
            agent = self.agents.get(agent_type)
            
            if not agent:
                logger.warning(f"No agent found for type: {agent_type}")
                agent = self.agents["customer_service"]
                agent_type = "customer_service"
            
            # Generate response
            response = await agent.generate_response(
                message=message,
                context=full_context,
                history=history
            )
            
            # Save to session
            await self.session_manager.add_message(
                user_id=user_id,
                role="user",
                content=message
            )
            await self.session_manager.add_message(
                user_id=user_id,
                role="assistant",
                content=response
            )
            
            return {
                "message": response,
                "agent_type": agent_type,
                "metadata": {
                    "intent": intent.get("intent"),
                    "confidence": intent.get("confidence"),
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def _select_agent(self, intent: Dict[str, Any]) -> str:
        """
        Select appropriate agent based on intent.
        
        Args:
            intent: Classified intent
        
        Returns:
            Agent type name
        """
        intent_type = intent.get("intent", "general")
        
        # Map intents to agents
        intent_mapping = {
            "product_inquiry": "sales",
            "order_status": "customer_service",
            "complaint": "customer_service",
            "technical_issue": "technical_support",
            "pet_diagnosis": "pet_diagnosis",
            "general": "customer_service",
        }
        
        return intent_mapping.get(intent_type, "customer_service")
