from app.wireguard import (
    WireGuardConfigParser,
    WireGuardKeyManager,
    WireGuardConfigValidator
)
from pathlib import Path
import os

def main():
    # Verwende das echte WireGuard-Verzeichnis
    wireguard_dir = "/etc/wireguard"
    print(f"Verwende WireGuard-Konfiguration aus: {wireguard_dir}")
    
    # Überprüfe Verzeichnis und Berechtigungen
    if not os.path.exists(wireguard_dir):
        print(f"Fehler: Verzeichnis {wireguard_dir} existiert nicht")
        return
    
    # Liste verfügbare Dateien
    print("\nVerfügbare Dateien:")
    try:
        for file in os.listdir(wireguard_dir):
            print(f"- {file} (Berechtigungen: {oct(os.stat(os.path.join(wireguard_dir, file)).st_mode)[-3:]})")
    except PermissionError:
        print("Keine Berechtigung zum Lesen des Verzeichnisses")
        return
    
    # 1. Konfiguration parsen
    print("\n1. Aktuelle WireGuard-Konfiguration:")
    parser = WireGuardConfigParser(wireguard_dir)
    try:
        if not os.path.exists(os.path.join(wireguard_dir, "wg0.conf")):
            print("Keine wg0.conf Datei gefunden")
            return
            
        config = parser.parse_config("wg0.conf")
        print("\nInterface-Konfiguration:")
        print(f"Address: {config.address}")
        print(f"Listen Port: {config.listen_port}")
        
        print(f"\nAnzahl der Peers: {len(config.peers)}")
        for i, peer in enumerate(config.peers, 1):
            print(f"\nPeer {i}:")
            print(f"Public Key: {peer.public_key[:10]}...")
            print(f"Allowed IPs: {peer.allowed_ips}")
            if peer.endpoint:
                print(f"Endpoint: {peer.endpoint}")
            if peer.persistent_keepalive:
                print(f"Persistent Keepalive: {peer.persistent_keepalive}")
    
    except PermissionError as e:
        print(f"Keine Berechtigung zum Lesen der Konfigurationsdatei: {e}")
        return
    except Exception as e:
        print(f"Fehler beim Parsen der Konfiguration: {e}")
        return

    # 2. Konfiguration validieren
    print("\n2. Validierung der Konfiguration:")
    validator = WireGuardConfigValidator()
    
    # Interface-Konfiguration validieren
    interface_config = {
        'PrivateKey': config.private_key,
        'Address': ','.join(config.address),
        'ListenPort': str(config.listen_port) if config.listen_port else None
    }
    
    interface_errors = validator.validate_interface(interface_config)
    if interface_errors:
        print("\nValidierungsfehler in der Interface-Konfiguration:")
        for error in interface_errors:
            print(f"- {error.field}: {error.message}")
    else:
        print("\nInterface-Konfiguration ist gültig.")
    
    # Peer-Konfigurationen validieren
    for i, peer in enumerate(config.peers, 1):
        peer_config = {
            'PublicKey': peer.public_key,
            'AllowedIPs': ','.join(peer.allowed_ips)
        }
        if peer.endpoint:
            peer_config['Endpoint'] = peer.endpoint
        if peer.persistent_keepalive:
            peer_config['PersistentKeepalive'] = str(peer.persistent_keepalive)
        
        peer_errors = validator.validate_peer(peer_config)
        if peer_errors:
            print(f"\nValidierungsfehler in Peer {i}:")
            for error in peer_errors:
                print(f"- {error.field}: {error.message}")
        else:
            print(f"\nPeer {i} Konfiguration ist gültig.")

    # 3. Schlüssel überprüfen
    print("\n3. Überprüfung der Schlüsseldateien:")
    try:
        # Versuche die private/public Schlüssel zu laden
        private_key = Path(wireguard_dir) / "privatekey"
        public_key = Path(wireguard_dir) / "publickey"
        
        print("\nSchlüsseldateien:")
        if private_key.exists():
            print(f"- Private Key existiert: {private_key}")
            try:
                priv_perms = oct(private_key.stat().st_mode)[-3:]
                print(f"  Berechtigungen: {priv_perms}")
            except PermissionError:
                print("  Keine Berechtigung zum Lesen der Berechtigungen")
        else:
            print("- Private Key nicht gefunden")
            
        if public_key.exists():
            print(f"- Public Key existiert: {public_key}")
            try:
                pub_perms = oct(public_key.stat().st_mode)[-3:]
                print(f"  Berechtigungen: {pub_perms}")
            except PermissionError:
                print("  Keine Berechtigung zum Lesen der Berechtigungen")
        else:
            print("- Public Key nicht gefunden")
            
    except Exception as e:
        print(f"Fehler beim Überprüfen der Schlüssel: {e}")

if __name__ == "__main__":
    main() 