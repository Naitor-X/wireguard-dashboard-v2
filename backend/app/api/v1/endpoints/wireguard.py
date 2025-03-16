from fastapi import APIRouter, HTTPException, status
from app.services.wireguard_monitor import WireGuardMonitor
from app.schemas.wireguard import WireGuardStatus
from typing import Dict, Any

router = APIRouter()

# Singleton-Instanz des WireGuard-Monitors
wireguard_monitor = WireGuardMonitor(
    interface="wg0",
    status_dir="app/data/wireguard_status",
    check_interval=15,
    admin_subnet="10.10.10.0/24",
    user_subnet="10.10.11.0/24"
)

@router.get("/status", response_model=WireGuardStatus)
async def get_wireguard_status():
    """
    Gibt den aktuellen WireGuard-Status zurück.
    Für alle Benutzer verfügbar.
    """
    try:
        wg_status = await wireguard_monitor.get_current_status()
        if not wg_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Keine Statusdaten verfügbar"
            )
        return wg_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Abrufen des WireGuard-Status: {str(e)}"
        ) 