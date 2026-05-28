"""Main entry point for AI Service."""
import os
import uvicorn
from dotenv import load_dotenv

from gateway.app import app
from shared.logger import configure_logging, get_logger

# Load environment variables
load_dotenv()

# Configure logging
configure_logging()
logger = get_logger(__name__)


def main():
    """Start the application."""
    port = int(os.getenv("PORT", 8001))
    logger.info("🚀 Starting AI Communication Service")
    logger.info(f"📊 API Documentation: http://localhost:{port}/docs")
    logger.info(f"🔗 Health Check: http://localhost:{port}/api/v1/health")
    
    uvicorn.run(
        "gateway.app:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
