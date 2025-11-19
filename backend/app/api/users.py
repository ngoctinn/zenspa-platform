"""User API để lấy thông tin profile."""

from app.modules.user.user_routes import router

# Re-export the router
__all__ = ["router"]
