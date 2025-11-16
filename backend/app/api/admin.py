"""Admin API để quản lý roles và users."""

from app.modules.admin.admin_routes import router

# Re-export the router
__all__ = ["router"]
