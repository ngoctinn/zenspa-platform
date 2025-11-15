"""
API router aggregation.
Combines all API routers with versioning.
"""

from fastapi import APIRouter

from app.api.health import router as health_router
from app.core.config import settings
from app.modules.auth import auth_router

# Create versioned API router
api_router = APIRouter(prefix=f"/api/{settings.api_version}")

# Include routers
api_router.include_router(health_router)
api_router.include_router(auth_router)

# Future routers will be added here
# api_router.include_router(users_router)
# api_router.include_router(appointments_router)
