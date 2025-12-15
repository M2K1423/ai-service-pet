"""Main entry point for AI Service."""
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
    logger.info("🚀 Starting AI Communication Service")
    logger.info("📊 API Documentation: http://localhost:8000/docs")
    logger.info("🔗 Health Check: http://localhost:8000/api/v1/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
