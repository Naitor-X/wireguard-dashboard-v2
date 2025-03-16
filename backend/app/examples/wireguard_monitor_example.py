import asyncio
import json
import os
from pathlib import Path
from app.services.wireguard_monitor import WireGuardMonitor
from app.core.logging import logger

async def main():
    # Erstelle ein temporäres Verzeichnis für die Statusdaten
    temp_dir = Path("/tmp/wireguard-monitor-example")
    os.makedirs(temp_dir, exist_ok=True)
    
    logger.info(f"Verwende temporäres Verzeichnis: {temp_dir}")
    
    # Erstelle eine Instanz des WireGuard-Monitors
    monitor = WireGuardMonitor(
        interface="wg0",
        status_dir=str(temp_dir),
        check_interval=5,  # Kürzeres Intervall für das Beispiel
        admin_subnet="10.10.10.0/24",
        user_subnet="10.10.11.0/24"
    )
    
    # Starte den Monitor in einer Hintergrund-Task
    logger.info("Starte WireGuard-Monitor...")
    monitor_task = asyncio.create_task(monitor.start())
    
    try:
        # Warte 30 Sekunden und zeige dann den Status an
        for i in range(6):
            await asyncio.sleep(5)
            logger.info(f"Warte... {(i+1)*5} Sekunden vergangen")
            
            # Versuche, den aktuellen Status zu lesen
            status = await monitor.get_current_status()
            if status:
                logger.info(f"Aktueller Status: {json.dumps(status, indent=2)}")
            else:
                logger.warning("Keine Statusdaten verfügbar")
    
    finally:
        # Stoppe den Monitor
        logger.info("Stoppe WireGuard-Monitor...")
        monitor.stop()
        
        # Warte auf das Ende der Monitor-Task
        try:
            await asyncio.wait_for(monitor_task, timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout beim Warten auf das Ende des WireGuard-Monitors")

if __name__ == "__main__":
    asyncio.run(main()) 