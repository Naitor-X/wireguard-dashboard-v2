#!/usr/bin/env python3
import asyncio
import logging
import sys
from pathlib import Path

# Füge das Hauptverzeichnis zum Pfad hinzu, um die App-Module zu importieren
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.utils.system_operations import SecureSystemOperations

# Logger konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def main():
    """
    Demonstriert die Verwendung der sicheren Systemoperationen.
    """
    # Initialisiere die sicheren Systemoperationen mit Testverzeichnissen
    # Für Tests verwenden wir temporäre Verzeichnisse
    wireguard_dir = Path("/tmp/wireguard_test")
    backup_dir = Path("/tmp/wireguard_backup_test")
    
    # Erstelle die Verzeichnisse, falls sie nicht existieren
    wireguard_dir.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialisiere die sicheren Systemoperationen
    # Für Tests verwenden wir den aktuellen Benutzer statt root
    import os
    import pwd
    current_user = pwd.getpwuid(os.getuid()).pw_name
    
    ops = SecureSystemOperations(
        wireguard_dir=str(wireguard_dir),
        backup_dir=str(backup_dir),
        wireguard_user=current_user,
        wireguard_group=current_user
    )
    
    try:
        # 1. Schlüsselgenerierung demonstrieren
        logger.info("1. Schlüsselgenerierung demonstrieren")
        
        # Generiere einen privaten Schlüssel
        private_key = await ops.generate_private_key()
        logger.info(f"Privater Schlüssel generiert: {private_key[:10]}...")
        
        # Leite den öffentlichen Schlüssel ab
        public_key = await ops.derive_public_key(private_key)
        logger.info(f"Öffentlicher Schlüssel abgeleitet: {public_key[:10]}...")
        
        # Generiere einen Preshared-Key
        psk = await ops.generate_preshared_key()
        logger.info(f"Preshared-Key generiert: {psk[:10]}...")
        
        # Speichere die Schlüssel
        private_key_path = await ops.save_key(private_key, "server_private.key", is_private=True)
        public_key_path = await ops.save_key(public_key, "server_public.key", is_private=False)
        psk_path = await ops.save_key(psk, "peer1_psk.key", is_private=True)
        
        logger.info(f"Schlüssel gespeichert in: {private_key_path.parent}")
        
        # 2. Konfigurationsdatei-Erstellung demonstrieren
        logger.info("\n2. Konfigurationsdatei-Erstellung demonstrieren")
        
        # Erstelle eine Server-Konfiguration
        server_config_path = await ops.create_server_config(
            interface="wg0",
            private_key=private_key,
            address=["10.0.0.1/24"],
            listen_port=51820,
            peers=[
                {
                    "public_key": "Peer1PublicKeyPlaceholder",
                    "allowed_ips": ["10.0.0.2/32"],
                    "preshared_key": psk
                }
            ]
        )
        
        logger.info(f"Server-Konfiguration erstellt: {server_config_path}")
        
        # Erstelle eine Client-Konfiguration
        client_config_path = await ops.create_client_config(
            client_name="peer1",
            client_private_key="ClientPrivateKeyPlaceholder",
            client_address=["10.0.0.2/32"],
            server_public_key=public_key,
            server_endpoint="server.example.com:51820",
            allowed_ips=["0.0.0.0/0"],
            dns_servers=["1.1.1.1", "8.8.8.8"],
            preshared_key=psk
        )
        
        logger.info(f"Client-Konfiguration erstellt: {client_config_path}")
        
        # 3. Backup-Funktionalität demonstrieren
        logger.info("\n3. Backup-Funktionalität demonstrieren")
        
        # Erstelle ein Backup der Server-Konfiguration
        backup_path = await ops.backup_config("wg0")
        
        if backup_path:
            logger.info(f"Backup erstellt: {backup_path}")
            
            # Liste alle Backups auf
            backups = await ops.list_backups()
            logger.info(f"Verfügbare Backups: {len(backups)}")
            for backup in backups:
                logger.info(f"  - {backup['interface']} vom {backup['timestamp']}")
            
            # Demonstriere Wiederherstellung (nur für Testzwecke)
            # In der Praxis würde man hier einen anderen Pfad verwenden
            success = await ops.restore_config(backup_path, "wg0")
            logger.info(f"Wiederherstellung {'erfolgreich' if success else 'fehlgeschlagen'}")
        
        # 4. Sichere Dateisystem-Operationen demonstrieren
        logger.info("\n4. Sichere Dateisystem-Operationen demonstrieren")
        
        # Schreibe eine Testdatei
        test_file_path = wireguard_dir / "test_file.txt"
        success = await ops.secure_write_file(
            test_file_path,
            "Dies ist ein Test der sicheren Dateisystem-Operationen.",
            is_private=True
        )
        
        logger.info(f"Datei sicher geschrieben: {success}")
        
        # Lese die Testdatei
        content = await ops.secure_read_file(test_file_path)
        logger.info(f"Dateiinhalt: {content}")
        
        # Lösche die Testdatei sicher
        success = await ops.secure_delete_file(test_file_path)
        logger.info(f"Datei sicher gelöscht: {success}")
        
        # 5. WireGuard-Neustarts/Updates demonstrieren (nur Simulation)
        logger.info("\n5. WireGuard-Neustarts/Updates demonstrieren (Simulation)")
        
        # In einer echten Umgebung würden diese Befehle tatsächlich WireGuard steuern
        # Hier simulieren wir nur die Aufrufe
        logger.info("Hinweis: Die folgenden Operationen werden nur simuliert und nicht tatsächlich ausgeführt.")
        
        # Simuliere einen WireGuard-Neustart
        logger.info("Simuliere WireGuard-Neustart...")
        # await ops.restart_wireguard("wg0")
        
        # Simuliere ein WireGuard-Konfigurations-Update
        logger.info("Simuliere WireGuard-Konfigurations-Update...")
        # await ops.update_wireguard_config("wg0", server_config_path)
        
    except Exception as e:
        logger.error(f"Fehler bei der Demonstration: {e}")
    finally:
        # Aufräumen (in einer echten Umgebung würde man dies nicht tun)
        logger.info("\nAufräumen...")
        
        # Lösche die erstellten Dateien
        for file_path in wireguard_dir.glob("*"):
            await ops.secure_delete_file(file_path)
        
        for file_path in backup_dir.glob("*"):
            await ops.secure_delete_file(file_path)
        
        # Lösche die Testverzeichnisse
        try:
            wireguard_dir.rmdir()
            backup_dir.rmdir()
            logger.info("Testverzeichnisse gelöscht.")
        except Exception as e:
            logger.warning(f"Konnte Testverzeichnisse nicht löschen: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 