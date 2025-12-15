"""Application constants."""

# Agent types
AGENT_CUSTOMER_SERVICE = "customer_service"
AGENT_SALES = "sales"
AGENT_TECHNICAL_SUPPORT = "technical_support"

# Intent types
INTENT_PRODUCT_INQUIRY = "product_inquiry"
INTENT_ORDER_STATUS = "order_status"
INTENT_COMPLAINT = "complaint"
INTENT_TECHNICAL_ISSUE = "technical_issue"
INTENT_GENERAL = "general"

# Message roles
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"

# API response status
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_PENDING = "pending"

# External service types
SERVICE_ZALO = "zalo"
SERVICE_FACEBOOK = "facebook"
SERVICE_TELEGRAM = "telegram"

# AI model types
MODEL_GEMINI = "gemini"
MODEL_OPENAI = "openai"
MODEL_CLAUDE = "claude"

# Database collections
COLLECTION_CONVERSATIONS = "conversations"
COLLECTION_CUSTOMERS = "customers"
COLLECTION_PRODUCTS = "products"
COLLECTION_ORDERS = "orders"

# Cache TTL (seconds)
CACHE_TTL_SHORT = 300  # 5 minutes
CACHE_TTL_MEDIUM = 1800  # 30 minutes
CACHE_TTL_LONG = 3600  # 1 hour
