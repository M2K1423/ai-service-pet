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
    get_product_detail,
    get_all_products,
    # Category & Promotion tools
    get_categories,
    get_promotions
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
        get_product_detail,     # Xem chi tiết 1 sản phẩm
        get_all_products,       # Lấy danh sách sản phẩm
        get_categories,         # Lấy danh mục sản phẩm
        get_promotions         # Lấy khuyến mãi hiện tại
    ],
    add_history_to_context=True,
    markdown=True,
)


