"""
Configuration Settings
Cấu hình cho toàn bộ ứng dụng
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# API CONFIGURATION
# ============================================

class Settings:
    """Application settings."""
    
    # Store API Backend
    STORE_API_BASE_URL: str = os.getenv("B_PLATFORM_STORE_API", "http://localhost:9000")
    
    # Google API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # API Security
    API_KEYS: list = os.getenv("API_KEYS", "test-key-123,dev-key-456").split(",")
    
    # HTTP Client Settings
    HTTP_TIMEOUT: float = 30.0
    HTTP_MAX_RETRIES: int = 3
    
    # Agent Settings
    DEFAULT_MODEL: str = "gpt-4"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # API Endpoints
    PRODUCTS_ENDPOINT: str = "/products/search"
    PRODUCT_DETAIL_ENDPOINT: str = "/products/{sku}"
    CATEGORIES_ENDPOINT: str = "/categories"
    PROMOTIONS_ENDPOINT: str = "/promotions"
    ORDERS_ENDPOINT: str = "/orders"
    CUSTOMERS_ENDPOINT: str = "/customers"
    
    @classmethod
    def get_product_url(cls, sku: str = None) -> str:
        """Get full product URL."""
        if sku:
            return f"{cls.STORE_API_BASE_URL}{cls.PRODUCT_DETAIL_ENDPOINT.format(sku=sku)}"
        return f"{cls.STORE_API_BASE_URL}{cls.PRODUCTS_ENDPOINT}"
    
    @classmethod
    def get_category_url(cls) -> str:
        """Get full category URL."""
        return f"{cls.STORE_API_BASE_URL}{cls.CATEGORIES_ENDPOINT}"
    
    @classmethod
    def get_promotion_url(cls) -> str:
        """Get full promotion URL."""
        return f"{cls.STORE_API_BASE_URL}{cls.PROMOTIONS_ENDPOINT}"
    
    @classmethod
    def get_order_url(cls, order_id: str = None) -> str:
        """Get full order URL."""
        if order_id:
            return f"{cls.STORE_API_BASE_URL}{cls.ORDERS_ENDPOINT}/{order_id}"
        return f"{cls.STORE_API_BASE_URL}{cls.ORDERS_ENDPOINT}"
    
    @classmethod
    def get_customer_url(cls, customer_id: str = None) -> str:
        """Get full customer URL."""
        if customer_id:
            return f"{cls.STORE_API_BASE_URL}{cls.CUSTOMERS_ENDPOINT}/{customer_id}"
        return f"{cls.STORE_API_BASE_URL}{cls.CUSTOMERS_ENDPOINT}"

# Singleton instance
settings = Settings()
