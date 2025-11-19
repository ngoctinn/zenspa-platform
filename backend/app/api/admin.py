"""Admin API để quản lý roles và users."""

from app.modules.user.user_routes import admin_router as router

# Re-export the router
__all__ = ["router"]
