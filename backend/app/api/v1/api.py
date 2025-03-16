from fastapi import APIRouter
from app.api.v1.endpoints import health, wireguard, system_operations

router = APIRouter()

# Health-Check-Router einbinden
router.include_router(health.router, tags=["health"])

# WireGuard-Router einbinden
router.include_router(wireguard.router, prefix="/wireguard", tags=["wireguard"])

# System-Operations-Router einbinden
router.include_router(system_operations.router, prefix="/system", tags=["system"])

# Hier werden später weitere Router eingebunden:
# router.include_router(wireguard_router, prefix="/wireguard", tags=["wireguard"]) 