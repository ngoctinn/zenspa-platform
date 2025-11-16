"""User API để lấy thông tin profile."""

from fastapi import APIRouter
from app.modules.customer.customer_routes import router as customer_router

# Include customer routes
router = APIRouter()
router.include_router(customer_router, tags=["users"])
