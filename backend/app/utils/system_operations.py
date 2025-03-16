import os
import subprocess
import shutil
import logging
import secrets
import base64
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import asyncio
import json
import stat
import pwd
import grp

# Logger konfigurieren
logger = logging.getLogger(__name__)

class SecureSystemOperations:
    """
    Sichere Systemoperationen für WireGuard-Dashboard.
    Implementiert Operationen mit minimalen Berechtigungen und sicheren Praktiken.
    """
    
    def __init__(
        self,
        wireguard_dir: str = "/etc/wireguard",
        backup_dir: str = "/var/backups/wireguard",
        wireguard_user: str = "root",
        wireguard_group: str = "root",
        sudo_path: str = "/usr/bin/sudo"
    ):
        """
        Initialisiert die sicheren Systemoperationen.
        
        Args:
            wireguard_dir: Verzeichnis für WireGuard-Konfigurationen
            backup_dir: Verzeichnis für Backups
            wireguard_user: Benutzer für WireGuard-Dateien
            wireguard_group: Gruppe für WireGuard-Dateien
            sudo_path: Pfad zum sudo-Befehl
        """
        self.wireguard_dir = Path(wireguard_dir)
        self.backup_dir = Path(backup_dir)
        self.wireguard_user = wireguard_user
        self.wireguard_group = wireguard_group
        self.sudo_path = sudo_path
        
        # Stelle sicher, dass die Verzeichnisse existieren
        self._ensure_dirs_exist()
    
    def _ensure_dirs_exist(self):
        """Stellt sicher, dass die benötigten Verzeichnisse existieren und die richtigen Berechtigungen haben."""
        # Wireguard-Verzeichnis
        if not self.wireguard_dir.exists():
            os.makedirs(self.wireguard_dir, mode=0o700, exist_ok=True)
            self._set_ownership(self.wireguard_dir)
        
        # Backup-Verzeichnis
        if not self.backup_dir.exists():
            os.makedirs(self.backup_dir, mode=0o700, exist_ok=True)
            self._set_ownership(self.backup_dir)
    
    def _set_ownership(self, path: Path):
        """Setzt die Eigentümerschaft für eine Datei oder ein Verzeichnis."""
        try:
            # Benutzer- und Gruppen-IDs abrufen
            uid = pwd.getpwnam(self.wireguard_user).pw_uid
            gid = grp.getgrnam(self.wireguard_group).gr_gid
            
            # Eigentümerschaft setzen
            os.chown(path, uid, gid)
            
            # Bei Verzeichnissen rekursiv für alle Dateien setzen
            if path.is_dir():
                for item in path.glob('**/*'):
                    os.chown(item, uid, gid)
        except (KeyError, PermissionError) as e:
            logger.error(f"Fehler beim Setzen der Eigentümerschaft für {path}: {e}")
    
    def _secure_file_permissions(self, file_path: Path, is_private: bool = False):
        """Setzt sichere Dateiberechtigungen."""
        if is_private:
            # Private Dateien (z.B. private Schlüssel): nur Besitzer darf lesen/schreiben
            file_path.chmod(0o600)
        else:
            # Öffentliche Dateien: Besitzer darf lesen/schreiben, Gruppe darf lesen
            file_path.chmod(0o640)
        
        self._set_ownership(file_path)
    
    async def _run_with_sudo(self, command: List[str]) -> Tuple[int, str, str]:
        """Führt einen Befehl mit sudo aus."""
        full_command = [self.sudo_path] + command
        
        process = await asyncio.create_subprocess_exec(
            *full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()
    
    # Schlüsselgenerierung
    
    async def generate_private_key(self) -> str:
        """
        Generiert einen sicheren WireGuard-Privatschlüssel.
        
        Returns:
            Der generierte Privatschlüssel als Base64-String.
        """
        try:
            # Methode 1: Verwende wg direkt (bevorzugt)
            returncode, stdout, stderr = await self._run_with_sudo(["wg", "genkey"])
            
            if returncode == 0:
                return stdout.strip()
            
            logger.warning(f"Konnte wg genkey nicht ausführen: {stderr}. Verwende Fallback-Methode.")
            
            # Methode 2: Fallback mit Python's secrets-Modul
            private_key = base64.b64encode(secrets.token_bytes(32)).decode('ascii')
            return private_key
            
        except Exception as e:
            logger.error(f"Fehler bei der Privatschlüsselgenerierung: {e}")
            raise RuntimeError(f"Privatschlüsselgenerierung fehlgeschlagen: {e}")
    
    async def derive_public_key(self, private_key: str) -> str:
        """
        Leitet den öffentlichen Schlüssel vom privaten Schlüssel ab.
        
        Args:
            private_key: Der private WireGuard-Schlüssel.
            
        Returns:
            Der abgeleitete öffentliche Schlüssel.
        """
        try:
            # Erstelle temporäre Datei für den privaten Schlüssel
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_path = temp_file.name
                temp_file.write(private_key)
            
            # Setze sichere Berechtigungen
            os.chmod(temp_path, 0o600)
            
            # Führe wg pubkey aus
            returncode, stdout, stderr = await self._run_with_sudo(
                ["wg", "pubkey"], 
                stdin=private_key.encode()
            )
            
            # Lösche die temporäre Datei
            os.unlink(temp_path)
            
            if returncode == 0:
                return stdout.strip()
            
            raise RuntimeError(f"Fehler beim Ableiten des öffentlichen Schlüssels: {stderr}")
            
        except Exception as e:
            logger.error(f"Fehler beim Ableiten des öffentlichen Schlüssels: {e}")
            raise RuntimeError(f"Ableiten des öffentlichen Schlüssels fehlgeschlagen: {e}")
    
    async def generate_preshared_key(self) -> str:
        """
        Generiert einen Preshared-Key für zusätzliche Sicherheit.
        
        Returns:
            Der generierte Preshared-Key als Base64-String.
        """
        try:
            # Methode 1: Verwende wg direkt (bevorzugt)
            returncode, stdout, stderr = await self._run_with_sudo(["wg", "genpsk"])
            
            if returncode == 0:
                return stdout.strip()
            
            logger.warning(f"Konnte wg genpsk nicht ausführen: {stderr}. Verwende Fallback-Methode.")
            
            # Methode 2: Fallback mit Python's secrets-Modul
            psk = base64.b64encode(secrets.token_bytes(32)).decode('ascii')
            return psk
            
        except Exception as e:
            logger.error(f"Fehler bei der Preshared-Key-Generierung: {e}")
            raise RuntimeError(f"Preshared-Key-Generierung fehlgeschlagen: {e}")
    
    async def save_key(self, key: str, filename: str, is_private: bool = False) -> Path:
        """
        Speichert einen Schlüssel sicher auf der Festplatte.
        
        Args:
            key: Der zu speichernde Schlüssel.
            filename: Der Dateiname ohne Pfad.
            is_private: Ob es sich um einen privaten Schlüssel handelt.
            
        Returns:
            Der Pfad zur gespeicherten Schlüsseldatei.
        """
        key_path = self.wireguard_dir / filename
        
        # Verwende temporäre Datei und verschiebe sie, um Race Conditions zu vermeiden
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(key)
        
        # Setze Berechtigungen für die temporäre Datei
        self._secure_file_permissions(temp_path, is_private)
        
        # Verschiebe die temporäre Datei an den Zielort
        shutil.move(temp_path, key_path)
        
        # Setze Berechtigungen für die Zieldatei
        self._secure_file_permissions(key_path, is_private)
        
        return key_path
    
    # Konfigurationsdatei-Erstellung
    
    async def create_server_config(
        self,
        interface: str,
        private_key: str,
        address: List[str],
        listen_port: int,
        peers: List[Dict[str, Any]]
    ) -> Path:
        """
        Erstellt eine sichere WireGuard-Serverkonfigurationsdatei.
        
        Args:
            interface: Name des WireGuard-Interfaces (z.B. wg0).
            private_key: Der private Schlüssel des Servers.
            address: Liste der IP-Adressen für das Interface.
            listen_port: Der Port, auf dem der Server lauscht.
            peers: Liste der Peer-Konfigurationen.
            
        Returns:
            Der Pfad zur erstellten Konfigurationsdatei.
        """
        config_path = self.wireguard_dir / f"{interface}.conf"
        
        # Erstelle Konfigurationsinhalt
        config_content = "[Interface]\n"
        config_content += f"PrivateKey = {private_key}\n"
        config_content += f"Address = {', '.join(address)}\n"
        config_content += f"ListenPort = {listen_port}\n\n"
        
        # Füge Peers hinzu
        for peer in peers:
            config_content += "[Peer]\n"
            config_content += f"PublicKey = {peer['public_key']}\n"
            
            if 'preshared_key' in peer and peer['preshared_key']:
                config_content += f"PresharedKey = {peer['preshared_key']}\n"
                
            config_content += f"AllowedIPs = {', '.join(peer['allowed_ips'])}\n"
            
            if 'endpoint' in peer and peer['endpoint']:
                config_content += f"Endpoint = {peer['endpoint']}\n"
                
            if 'persistent_keepalive' in peer and peer['persistent_keepalive']:
                config_content += f"PersistentKeepalive = {peer['persistent_keepalive']}\n"
                
            config_content += "\n"
        
        # Schreibe Konfiguration in temporäre Datei
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(config_content)
        
        # Setze Berechtigungen für die temporäre Datei
        self._secure_file_permissions(temp_path, is_private=True)
        
        # Verschiebe die temporäre Datei an den Zielort
        shutil.move(temp_path, config_path)
        
        # Setze Berechtigungen für die Zieldatei
        self._secure_file_permissions(config_path, is_private=True)
        
        return config_path
    
    async def create_client_config(
        self,
        client_name: str,
        client_private_key: str,
        client_address: List[str],
        server_public_key: str,
        server_endpoint: str,
        allowed_ips: List[str],
        dns_servers: Optional[List[str]] = None,
        preshared_key: Optional[str] = None,
        persistent_keepalive: Optional[int] = 25
    ) -> Path:
        """
        Erstellt eine WireGuard-Clientkonfigurationsdatei.
        
        Args:
            client_name: Name des Clients.
            client_private_key: Der private Schlüssel des Clients.
            client_address: Liste der IP-Adressen für den Client.
            server_public_key: Der öffentliche Schlüssel des Servers.
            server_endpoint: Der Endpunkt des Servers (IP:Port).
            allowed_ips: Liste der erlaubten IPs für den Client.
            dns_servers: Optionale Liste von DNS-Servern.
            preshared_key: Optionaler Preshared-Key für zusätzliche Sicherheit.
            persistent_keepalive: Optionaler Keepalive-Wert in Sekunden.
            
        Returns:
            Der Pfad zur erstellten Konfigurationsdatei.
        """
        config_path = self.wireguard_dir / f"{client_name}.conf"
        
        # Erstelle Konfigurationsinhalt
        config_content = "[Interface]\n"
        config_content += f"PrivateKey = {client_private_key}\n"
        config_content += f"Address = {', '.join(client_address)}\n"
        
        if dns_servers:
            config_content += f"DNS = {', '.join(dns_servers)}\n"
        
        config_content += "\n[Peer]\n"
        config_content += f"PublicKey = {server_public_key}\n"
        
        if preshared_key:
            config_content += f"PresharedKey = {preshared_key}\n"
            
        config_content += f"AllowedIPs = {', '.join(allowed_ips)}\n"
        config_content += f"Endpoint = {server_endpoint}\n"
        
        if persistent_keepalive:
            config_content += f"PersistentKeepalive = {persistent_keepalive}\n"
        
        # Schreibe Konfiguration in temporäre Datei
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(config_content)
        
        # Setze Berechtigungen für die temporäre Datei
        self._secure_file_permissions(temp_path, is_private=True)
        
        # Verschiebe die temporäre Datei an den Zielort
        shutil.move(temp_path, config_path)
        
        # Setze Berechtigungen für die Zieldatei
        self._secure_file_permissions(config_path, is_private=True)
        
        return config_path
    
    # WireGuard-Neustarts/Updates
    
    async def restart_wireguard(self, interface: str) -> bool:
        """
        Startet ein WireGuard-Interface neu.
        
        Args:
            interface: Name des WireGuard-Interfaces (z.B. wg0).
            
        Returns:
            True, wenn der Neustart erfolgreich war, sonst False.
        """
        try:
            # Führe wg-quick down und up aus
            logger.info(f"Starte WireGuard-Interface {interface} neu...")
            
            # Interface herunterfahren
            returncode, stdout, stderr = await self._run_with_sudo(
                ["wg-quick", "down", interface]
            )
            
            if returncode != 0:
                logger.error(f"Fehler beim Herunterfahren von {interface}: {stderr}")
                return False
            
            # Kurze Pause
            await asyncio.sleep(1)
            
            # Interface hochfahren
            returncode, stdout, stderr = await self._run_with_sudo(
                ["wg-quick", "up", interface]
            )
            
            if returncode != 0:
                logger.error(f"Fehler beim Hochfahren von {interface}: {stderr}")
                return False
            
            logger.info(f"WireGuard-Interface {interface} erfolgreich neu gestartet.")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Neustart von WireGuard: {e}")
            return False
    
    async def update_wireguard_config(self, interface: str, config_path: Path) -> bool:
        """
        Aktualisiert die Konfiguration eines laufenden WireGuard-Interfaces.
        
        Args:
            interface: Name des WireGuard-Interfaces (z.B. wg0).
            config_path: Pfad zur neuen Konfigurationsdatei.
            
        Returns:
            True, wenn das Update erfolgreich war, sonst False.
        """
        try:
            # Prüfe, ob die Konfigurationsdatei existiert
            if not config_path.exists():
                logger.error(f"Konfigurationsdatei {config_path} existiert nicht.")
                return False
            
            # Prüfe, ob das Interface aktiv ist
            returncode, stdout, stderr = await self._run_with_sudo(
                ["wg", "show", interface]
            )
            
            if returncode != 0:
                # Interface ist nicht aktiv, starte es neu
                logger.info(f"Interface {interface} ist nicht aktiv. Starte es neu...")
                return await self.restart_wireguard(interface)
            
            # Interface ist aktiv, aktualisiere die Konfiguration
            logger.info(f"Aktualisiere Konfiguration für Interface {interface}...")
            
            # Sichere die aktuelle Konfiguration
            await self.backup_config(interface)
            
            # Aktualisiere die Konfiguration
            returncode, stdout, stderr = await self._run_with_sudo(
                ["wg", "syncconf", interface, str(config_path)]
            )
            
            if returncode != 0:
                logger.error(f"Fehler beim Aktualisieren der Konfiguration: {stderr}")
                return False
            
            logger.info(f"Konfiguration für Interface {interface} erfolgreich aktualisiert.")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Aktualisieren der WireGuard-Konfiguration: {e}")
            return False
    
    # Backup-Funktionalität
    
    async def backup_config(self, interface: str) -> Optional[Path]:
        """
        Erstellt ein Backup der aktuellen WireGuard-Konfiguration.
        
        Args:
            interface: Name des WireGuard-Interfaces (z.B. wg0).
            
        Returns:
            Der Pfad zum Backup oder None, wenn das Backup fehlgeschlagen ist.
        """
        try:
            # Stelle sicher, dass das Backup-Verzeichnis existiert
            if not self.backup_dir.exists():
                os.makedirs(self.backup_dir, mode=0o700, exist_ok=True)
                self._set_ownership(self.backup_dir)
            
            # Pfad zur Konfigurationsdatei
            config_path = self.wireguard_dir / f"{interface}.conf"
            
            if not config_path.exists():
                logger.warning(f"Konfigurationsdatei {config_path} existiert nicht. Kein Backup erstellt.")
                return None
            
            # Erstelle Backup-Dateinamen mit Zeitstempel
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"{interface}_{timestamp}.conf"
            
            # Kopiere die Konfigurationsdatei
            shutil.copy2(config_path, backup_path)
            
            # Setze sichere Berechtigungen für das Backup
            self._secure_file_permissions(backup_path, is_private=True)
            
            logger.info(f"Backup der Konfiguration für {interface} erstellt: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des Backups: {e}")
            return None
    
    async def restore_config(self, backup_path: Path, interface: str) -> bool:
        """
        Stellt eine WireGuard-Konfiguration aus einem Backup wieder her.
        
        Args:
            backup_path: Pfad zur Backup-Datei.
            interface: Name des WireGuard-Interfaces (z.B. wg0).
            
        Returns:
            True, wenn die Wiederherstellung erfolgreich war, sonst False.
        """
        try:
            # Prüfe, ob die Backup-Datei existiert
            if not backup_path.exists():
                logger.error(f"Backup-Datei {backup_path} existiert nicht.")
                return False
            
            # Pfad zur Konfigurationsdatei
            config_path = self.wireguard_dir / f"{interface}.conf"
            
            # Erstelle ein Backup der aktuellen Konfiguration, falls vorhanden
            if config_path.exists():
                await self.backup_config(interface)
            
            # Kopiere die Backup-Datei zur Konfigurationsdatei
            shutil.copy2(backup_path, config_path)
            
            # Setze sichere Berechtigungen für die Konfigurationsdatei
            self._secure_file_permissions(config_path, is_private=True)
            
            # Starte das Interface neu
            success = await self.restart_wireguard(interface)
            
            if success:
                logger.info(f"Konfiguration für {interface} erfolgreich wiederhergestellt.")
            else:
                logger.error(f"Fehler beim Neustart von {interface} nach Wiederherstellung.")
            
            return success
            
        except Exception as e:
            logger.error(f"Fehler bei der Wiederherstellung der Konfiguration: {e}")
            return False
    
    async def list_backups(self, interface: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Listet alle verfügbaren Backups auf.
        
        Args:
            interface: Optionaler Name des WireGuard-Interfaces, um die Backups zu filtern.
            
        Returns:
            Eine Liste von Backup-Informationen.
        """
        try:
            # Stelle sicher, dass das Backup-Verzeichnis existiert
            if not self.backup_dir.exists():
                return []
            
            # Suche nach Backup-Dateien
            pattern = f"{interface}_*.conf" if interface else "*.conf"
            backup_files = list(self.backup_dir.glob(pattern))
            
            # Sortiere nach Änderungsdatum (neueste zuerst)
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Erstelle Informationen für jedes Backup
            backups = []
            for backup_file in backup_files:
                # Extrahiere Interface-Namen und Zeitstempel aus dem Dateinamen
                filename = backup_file.name
                parts = filename.split('_', 1)
                
                if len(parts) == 2:
                    interface_name = parts[0]
                    timestamp_str = parts[1].replace('.conf', '')
                    
                    try:
                        # Versuche, den Zeitstempel zu parsen
                        timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    except ValueError:
                        # Fallback: Verwende die Änderungszeit der Datei
                        timestamp = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    
                    backups.append({
                        'interface': interface_name,
                        'path': str(backup_file),
                        'timestamp': timestamp.isoformat(),
                        'size': backup_file.stat().st_size
                    })
            
            return backups
            
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der Backups: {e}")
            return []
    
    # Sichere Dateisystem-Operationen
    
    async def secure_delete_file(self, file_path: Path) -> bool:
        """
        Löscht eine Datei sicher, indem sie vor dem Löschen überschrieben wird.
        
        Args:
            file_path: Pfad zur zu löschenden Datei.
            
        Returns:
            True, wenn das Löschen erfolgreich war, sonst False.
        """
        try:
            if not file_path.exists():
                logger.warning(f"Datei {file_path} existiert nicht.")
                return True
            
            # Dateigröße ermitteln
            file_size = file_path.stat().st_size
            
            # Datei mit Zufallsdaten überschreiben
            with open(file_path, 'wb') as f:
                # Überschreibe die Datei dreimal
                for _ in range(3):
                    f.seek(0)
                    f.write(secrets.token_bytes(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Datei löschen
            file_path.unlink()
            
            logger.info(f"Datei {file_path} sicher gelöscht.")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim sicheren Löschen der Datei {file_path}: {e}")
            return False
    
    async def secure_read_file(self, file_path: Path) -> Optional[str]:
        """
        Liest eine Datei sicher ein.
        
        Args:
            file_path: Pfad zur zu lesenden Datei.
            
        Returns:
            Der Inhalt der Datei oder None, wenn das Lesen fehlgeschlagen ist.
        """
        try:
            if not file_path.exists():
                logger.error(f"Datei {file_path} existiert nicht.")
                return None
            
            # Prüfe Berechtigungen
            file_stat = file_path.stat()
            
            # Prüfe, ob die Datei für andere lesbar ist
            if file_stat.st_mode & stat.S_IROTH:
                logger.warning(f"Datei {file_path} ist für andere lesbar. Setze sichere Berechtigungen.")
                file_path.chmod(file_stat.st_mode & ~stat.S_IROTH)
            
            # Lese die Datei
            content = file_path.read_text()
            
            return content
            
        except Exception as e:
            logger.error(f"Fehler beim sicheren Lesen der Datei {file_path}: {e}")
            return None
    
    async def secure_write_file(self, file_path: Path, content: str, is_private: bool = False) -> bool:
        """
        Schreibt Inhalt sicher in eine Datei.
        
        Args:
            file_path: Pfad zur zu schreibenden Datei.
            content: Der zu schreibende Inhalt.
            is_private: Ob es sich um eine private Datei handelt.
            
        Returns:
            True, wenn das Schreiben erfolgreich war, sonst False.
        """
        try:
            # Erstelle temporäre Datei
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(content)
            
            # Setze Berechtigungen für die temporäre Datei
            self._secure_file_permissions(temp_path, is_private)
            
            # Erstelle Verzeichnis, falls es nicht existiert
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Verschiebe die temporäre Datei an den Zielort
            shutil.move(temp_path, file_path)
            
            # Setze Berechtigungen für die Zieldatei
            self._secure_file_permissions(file_path, is_private)
            
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim sicheren Schreiben der Datei {file_path}: {e}")
            return False 