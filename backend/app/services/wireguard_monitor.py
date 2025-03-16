import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Logger konfigurieren
logger = logging.getLogger(__name__)

class WireGuardMonitor:
    """
    Service zur Überwachung des WireGuard-Status.
    - Periodische Statusabfrage (15-Sekunden-Intervall)
    - Erfassung von Online-Status, IP-Adressen und letzter Aktivität
    - Speicherung der Statusdaten im JSON-Format
    - Ereignis-basierte Aktualisierung
    - Performance-optimierte Abfragen
    - Fehlertolerante Implementierung
    """
    
    def __init__(
        self,
        interface: str = "wg0",
        status_dir: str = "app/data/wireguard_status",
        check_interval: int = 15,
        admin_subnet: str = "10.10.10.0/24",
        user_subnet: str = "10.10.11.0/24"
    ):
        """
        Initialisiert den WireGuard-Monitor.
        
        Args:
            interface: Name des WireGuard-Interfaces (Standard: wg0)
            status_dir: Verzeichnis für die Speicherung der Statusdaten
            check_interval: Intervall für die Statusabfrage in Sekunden
            admin_subnet: Subnetz für Administratoren
            user_subnet: Subnetz für normale Benutzer
        """
        self.interface = interface
        self.status_dir = Path(status_dir)
        self.check_interval = check_interval
        self.admin_subnet = admin_subnet
        self.user_subnet = user_subnet
        self.running = False
        self.last_status: Dict[str, Any] = {}
        
        # Stelle sicher, dass das Statusverzeichnis existiert
        os.makedirs(self.status_dir, exist_ok=True)
        
        # Pfad zur Statusdatei
        self.status_file = self.status_dir / f"{interface}_status.json"
    
    async def start(self):
        """Startet den Monitoring-Service."""
        if self.running:
            logger.warning("WireGuard-Monitor läuft bereits.")
            return
        
        self.running = True
        logger.info(f"WireGuard-Monitor für Interface {self.interface} gestartet.")
        
        try:
            while self.running:
                try:
                    await self._check_status()
                except Exception as e:
                    logger.error(f"Fehler bei der Statusabfrage: {e}")
                
                await asyncio.sleep(self.check_interval)
        except asyncio.CancelledError:
            logger.info("WireGuard-Monitor wurde beendet.")
            self.running = False
    
    def stop(self):
        """Stoppt den Monitoring-Service."""
        self.running = False
        logger.info("WireGuard-Monitor wird beendet.")
    
    async def _check_status(self):
        """Führt eine Statusabfrage durch und aktualisiert die Statusdaten."""
        try:
            # Führe 'wg show' aus, um den aktuellen Status zu erhalten
            process = await asyncio.create_subprocess_exec(
                "wg", "show", self.interface, "dump",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(f"Fehler bei der Ausführung von 'wg show': {error_msg}")
                return
            
            # Verarbeite die Ausgabe
            status_data = self._parse_wg_dump(stdout.decode())
            
            # Speichere die Statusdaten
            await self._save_status(status_data)
            
            # Prüfe auf Änderungen
            if self._has_status_changed(status_data):
                logger.info(f"WireGuard-Status für {self.interface} hat sich geändert.")
                self.last_status = status_data
        
        except Exception as e:
            logger.error(f"Fehler bei der Statusabfrage: {e}")
    
    def _parse_wg_dump(self, dump_output: str) -> Dict[str, Any]:
        """
        Parst die Ausgabe von 'wg show <interface> dump'.
        
        Format der Ausgabe:
        <interface_public_key> <interface_private_key> <listen_port> <fwmark>
        <peer_public_key> <preshared_key> <endpoint> <allowed_ips> <latest_handshake> <transfer_rx> <transfer_tx> <persistent_keepalive>
        
        Returns:
            Dict mit den Statusdaten
        """
        lines = dump_output.strip().split('\n')
        status = {
            "timestamp": datetime.now().isoformat(),
            "interface": self.interface,
            "peers": []
        }
        
        # Erste Zeile enthält Interface-Informationen
        if lines:
            interface_parts = lines[0].split('\t')
            if len(interface_parts) >= 3:
                status["public_key"] = interface_parts[0]
                status["listen_port"] = interface_parts[2]
        
        # Restliche Zeilen enthalten Peer-Informationen
        for i in range(1, len(lines)):
            peer_parts = lines[i].split('\t')
            if len(peer_parts) >= 8:
                peer = {
                    "public_key": peer_parts[0],
                    "endpoint": peer_parts[2] if peer_parts[2] else None,
                    "allowed_ips": peer_parts[3].split(',') if peer_parts[3] else [],
                    "latest_handshake": int(peer_parts[4]) if peer_parts[4] else 0,
                    "transfer_rx": int(peer_parts[5]) if peer_parts[5] else 0,
                    "transfer_tx": int(peer_parts[6]) if peer_parts[6] else 0,
                    "persistent_keepalive": peer_parts[7] if peer_parts[7] else None
                }
                
                # Berechne zusätzliche Informationen
                peer["online"] = (time.time() - peer["latest_handshake"]) < 180 if peer["latest_handshake"] > 0 else False
                peer["last_activity"] = datetime.fromtimestamp(peer["latest_handshake"]).isoformat() if peer["latest_handshake"] > 0 else None
                
                # Bestimme den Benutzertyp basierend auf dem Subnetz
                peer["type"] = self._determine_peer_type(peer["allowed_ips"])
                
                status["peers"].append(peer)
        
        return status
    
    def _determine_peer_type(self, allowed_ips: List[str]) -> str:
        """
        Bestimmt den Typ des Peers basierend auf den erlaubten IP-Adressen.
        
        Args:
            allowed_ips: Liste der erlaubten IP-Adressen
            
        Returns:
            "admin" für Administratoren, "user" für normale Benutzer, "unknown" sonst
        """
        for ip in allowed_ips:
            if ip.startswith(self.admin_subnet.split('/')[0].rsplit('.', 1)[0]):
                return "admin"
            elif ip.startswith(self.user_subnet.split('/')[0].rsplit('.', 1)[0]):
                return "user"
        return "unknown"
    
    async def _save_status(self, status: Dict[str, Any]):
        """
        Speichert die Statusdaten im JSON-Format.
        
        Args:
            status: Statusdaten
        """
        try:
            # Schreibe die Daten in eine temporäre Datei und benenne sie dann um,
            # um atomare Schreibvorgänge zu gewährleisten
            temp_file = self.status_file.with_suffix('.tmp')
            
            with open(temp_file, 'w') as f:
                json.dump(status, f, indent=2)
            
            # Atomares Umbenennen
            os.replace(temp_file, self.status_file)
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Statusdaten: {e}")
    
    def _has_status_changed(self, new_status: Dict[str, Any]) -> bool:
        """
        Prüft, ob sich der Status geändert hat.
        
        Args:
            new_status: Neuer Status
            
        Returns:
            True, wenn sich der Status geändert hat, sonst False
        """
        if not self.last_status:
            return True
        
        # Vergleiche die Anzahl der Peers
        if len(new_status.get("peers", [])) != len(self.last_status.get("peers", [])):
            return True
        
        # Vergleiche den Online-Status und die letzte Aktivität der Peers
        for new_peer in new_status.get("peers", []):
            found = False
            for old_peer in self.last_status.get("peers", []):
                if new_peer["public_key"] == old_peer["public_key"]:
                    found = True
                    if new_peer["online"] != old_peer["online"] or new_peer["latest_handshake"] != old_peer["latest_handshake"]:
                        return True
                    break
            
            if not found:
                return True
        
        return False
    
    async def get_current_status(self) -> Dict[str, Any]:
        """
        Gibt den aktuellen Status zurück.
        
        Returns:
            Aktueller Status oder leeres Dict, wenn keine Daten verfügbar sind
        """
        try:
            if self.status_file.exists():
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Fehler beim Lesen der Statusdaten: {e}")
            return {} 