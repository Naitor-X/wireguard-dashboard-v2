import asyncio
import json
import os
from pathlib import Path
from app.services.wireguard_monitor import WireGuardMonitor
from app.core.logging import logger

# Simulierte WireGuard-Daten für Testzwecke
SIMULATED_WG_DUMP = """ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCD	PRIVKEY	51820	off
PEER1PUBLICKEY0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMN	(none)	192.168.1.100:51820	10.10.10.2/32	1647432000	1024	2048	25
PEER2PUBLICKEY0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCDEFGHIJKLMN	(none)	192.168.1.101:51820	10.10.11.2/32	1647432100	2048	4096	25
"""

class MockWireGuardMonitor(WireGuardMonitor):
    """Eine Mock-Version des WireGuard-Monitors für Testzwecke."""
    
    async def _check_status(self):
        """Überschreibt die Statusabfrage mit simulierten Daten."""
        try:
            # Verwende simulierte Daten
            status_data = self._parse_wg_dump(SIMULATED_WG_DUMP)
            
            # Speichere die Statusdaten
            await self._save_status(status_data)
            
            # Prüfe auf Änderungen
            if self._has_status_changed(status_data):
                logger.info(f"WireGuard-Status für {self.interface} hat sich geändert.")
                self.last_status = status_data
        
        except Exception as e:
            logger.error(f"Fehler bei der Statusabfrage: {e}")

async def main():
    # Erstelle ein temporäres Verzeichnis für die Statusdaten
    temp_dir = Path("/tmp/wireguard-monitor-example")
    os.makedirs(temp_dir, exist_ok=True)
    
    logger.info(f"Verwende temporäres Verzeichnis: {temp_dir}")
    
    # Erstelle eine Instanz des Mock-WireGuard-Monitors
    monitor = MockWireGuardMonitor(
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