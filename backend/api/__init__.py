from fastapi import APIRouter
from .finance_router import router as finance_router

# Main API router that includes all sub-routers
router = APIRouter()

# Include finance router
router.include_router(finance_router)

# You can add more routers here as the application grows
# router.include_router(auth_router)
# router.include_router(user_router)

__all__ = ["router"]