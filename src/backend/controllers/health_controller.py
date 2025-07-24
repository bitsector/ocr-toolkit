# Health Controller - HTTP request/response handlers for health and system endpoints
# This layer handles HTTP-specific concerns like request validation, response formatting,
# error handling, and delegates business logic to the core layer.

from datetime import datetime
from typing import Dict, Any


class HealthController:
    """
    Controller for health and system status HTTP endpoints.
    Handles request/response processing for system health checks.
    """

    def get_root_status(self) -> Dict[str, Any]:
        """
        Handle root endpoint request.
        Returns basic API status information.
        """
        return {
            "message": "OCR Toolkit API is running",
            "status": "healthy"
        }

    def get_health_status(self) -> Dict[str, Any]:
        """
        Handle health check endpoint request.
        Returns detailed health status with timestamp.
        """
        return {
            "status": "healthy",
            "timestamp": datetime.now()
        }
