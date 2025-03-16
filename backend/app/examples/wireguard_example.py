from app.wireguard import (
    WireGuardConfigParser,
    WireGuardKeyManager,
    WireGuardConfigValidator,
    WireGuardConfig,
    WireGuardPeer
)
from pathlib import Path

def main():
    # Beispiel-Konfigurationsverzeichnis
    config_dir = Path("/tmp/wireguard-example")
    config_dir.mkdir(exist_ok=True)
    
    # 1. Schlüsselverwaltung
    print("1. Schlüsselverwaltung:")
    key_manager = WireGuardKeyManager(str(config_dir))
    
    # Generiere ein neues Schlüsselpaar für den Server
    server_keys = key_manager.generate_keypair()
    print(f"Server Private Key: {server_keys.private_key[:10]}...")
    print(f"Server Public Key: {server_keys.public_key[:10]}...")
    
    # Speichere die Schlüssel
    key_manager.save_keypair("server", server_keys)
    print("Schlüssel wurden gespeichert.")
    
    # 2. Konfigurationsvalidierung
    print("\n2. Konfigurationsvalidierung:")
    validator = WireGuardConfigValidator()
    
    # Beispiel-Interface-Konfiguration
    interface_config = {
        'PrivateKey': server_keys.private_key,
        'Address': '10.0.0.1/24',
        'ListenPort': '51820'
    }
    
    # Validiere Interface-Konfiguration
    errors = validator.validate_interface(interface_config)
    if errors:
        print("Validierungsfehler in der Interface-Konfiguration:")
        for error in errors:
            print(f"- {error.field}: {error.message}")
    else:
        print("Interface-Konfiguration ist gültig.")
    
    # 3. Konfigurationserstellung und -parsing
    print("\n3. Konfigurationserstellung und -parsing:")
    
    # Erstelle eine Beispiel-Konfigurationsdatei
    config_content = f"""[Interface]
PrivateKey = {server_keys.private_key}
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = {server_keys.public_key}  # Hier würde normalerweise der Public Key des Peers stehen
AllowedIPs = 10.0.0.2/32
Endpoint = example.com:51820
PersistentKeepalive = 25
"""
    
    # Speichere die Konfiguration
    config_file = config_dir / "wg0.conf"
    config_file.write_text(config_content)
    print(f"Beispiel-Konfiguration wurde in {config_file} gespeichert.")
    
    # Parse die Konfiguration
    parser = WireGuardConfigParser(str(config_dir))
    try:
        config = parser.parse_config("wg0.conf")
        print("\nGeparste Konfiguration:")
        print(f"Interface Address: {config.address}")
        print(f"Listen Port: {config.listen_port}")
        print(f"Anzahl Peers: {len(config.peers)}")
        
        # Zeige Details des ersten Peers
        if config.peers:
            peer = config.peers[0]
            print("\nErster Peer:")
            print(f"Public Key: {peer.public_key[:10]}...")
            print(f"Allowed IPs: {peer.allowed_ips}")
            print(f"Endpoint: {peer.endpoint}")
            print(f"Keepalive: {peer.persistent_keepalive}")
    
    except Exception as e:
        print(f"Fehler beim Parsen der Konfiguration: {e}")

if __name__ == "__main__":
    main() 