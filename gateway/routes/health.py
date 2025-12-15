"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Service Gateway"
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # Add checks for dependencies (DB, AI models, etc.)
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }
