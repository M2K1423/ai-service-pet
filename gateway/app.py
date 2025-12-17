"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.routes import chat, webhook, health
from gateway.middleware.logging import LoggingMiddleware
from gateway.middleware.deduplication import RequestDeduplicationMiddleware
from shared.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="AI Service Gateway",
    description="Gateway layer for AI communication service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(RequestDeduplicationMiddleware, window_seconds=30)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
# app.include_router(webhook.router, prefix="/api/v1", tags=["Webhook"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("🚀 AI Service Gateway starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("👋 AI Service Gateway shutting down...")
