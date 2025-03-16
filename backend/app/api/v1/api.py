from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, wireguard

router = APIRouter()

# Health-Check-Router einbinden
router.include_router(health.router, tags=["health"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])

# WireGuard-Router einbinden
router.include_router(wireguard.router, prefix="/wireguard", tags=["wireguard"])

# Hier werden später weitere Router eingebunden:
# router.include_router(wireguard_router, prefix="/wireguard", tags=["wireguard"]) 