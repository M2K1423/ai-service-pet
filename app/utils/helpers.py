"""Helper functions"""
from datetime import datetime


def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()


def format_response(data, status="success"):
    """Format API response"""
    return {
        "status": status,
        "data": data,
        "timestamp": get_timestamp()
    }
