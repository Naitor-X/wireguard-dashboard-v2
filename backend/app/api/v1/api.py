from fastapi import APIRouter
from .health import router as health_router

router = APIRouter()

# Health-Check-Router einbinden
router.include_router(health_router, tags=["health"])

# Hier werden später weitere Router eingebunden:
# router.include_router(auth_router, prefix="/auth", tags=["auth"])
# router.include_router(wireguard_router, prefix="/wireguard", tags=["wireguard"]) 