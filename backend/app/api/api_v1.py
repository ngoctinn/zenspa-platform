"""API v1 router - entry point cho tất cả API endpoints."""

from fastapi import APIRouter
from app.api.health import router as health_router
from app.modules.user.user_routes import router as users_router
from app.modules.user.user_routes import admin_router

# Tạo router có version
api_v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

# Bao gồm domain routers
api_v1_router.include_router(health_router, prefix="", tags=["health"])

api_v1_router.include_router(admin_router, prefix="/admin", tags=["admin"])

api_v1_router.include_router(users_router, prefix="/users", tags=["users"])

# Future: Bao gồm các domain routers khác
# api_v1_router.include_router(
#     appointment_router,
#     prefix="/appointments",
#     tags=["appointments"]
# )
# api_v1_router.include_router(
#     customer_router,
#     prefix="/customers",
#     tags=["customers"]
# )
# api_v1_router.include_router(
#     staff_router,
#     prefix="/staff",
#     tags=["staff"]
# )
# api_v1_router.include_router(
#     serviceline_router,
#     prefix="/servicelines",
#     tags=["servicelines"]
# )
# api_v1_router.include_router(
#     notification_router,
#     prefix="/notifications",
#     tags=["notifications"]
# )
