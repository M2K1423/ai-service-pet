"""
Agent Definitions và Logic
Định nghĩa các agents sử dụng tools để gọi Store API
Theo sơ đồ: Zalo/Messenger -> CRA Backend -> AI Agent -> Store API
"""
from agno.agent import Agent
from agno.models.ollama import Ollama
from src.core.prompts import SALES_PROMPT
from src.integrations.tools import (
    # Product tools
    search_products,
)

# ============================================
# AGENT DEFINITION
# ============================================

sales_agent = Agent(
    name="Sales Agent",
    model=Ollama(id="llama3.2"),
    instructions=SALES_PROMPT,
    tools=[
        search_products,        # Tìm kiếm sản phẩm theo filters
    ],
    add_history_to_context=True,
    markdown=True,
)


