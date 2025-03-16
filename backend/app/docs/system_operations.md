# Sichere Systemoperationen für WireGuard-Dashboard

Diese Dokumentation beschreibt die implementierten sicheren Systemoperationen für das WireGuard-Dashboard.

## Überblick

Die Klasse `SecureSystemOperations` implementiert sichere Systemoperationen für das WireGuard-Dashboard mit folgenden Funktionen:

1. **Schlüsselgenerierung**: Sichere Generierung von privaten, öffentlichen und Preshared-Keys
2. **Konfigurationsdatei-Erstellung**: Sichere Erstellung von Server- und Client-Konfigurationsdateien
3. **Sichere Dateisystem-Operationen**: Sichere Lese-, Schreib- und Löschoperationen
4. **WireGuard-Neustarts/Updates**: Sichere Neustarts und Updates von WireGuard-Interfaces
5. **Backup-Funktionalität**: Erstellung, Auflistung und Wiederherstellung von Backups

Alle Operationen werden mit minimalen Berechtigungen und sicheren Praktiken implementiert.

## Sicherheitsmaßnahmen

Die folgenden Sicherheitsmaßnahmen wurden implementiert:

### Minimale Berechtigungen

- Dateien werden mit minimalen Berechtigungen erstellt (600 für private Dateien, 640 für öffentliche Dateien)
- Verzeichnisse werden mit minimalen Berechtigungen erstellt (700)
- Eigentümerschaft wird auf den WireGuard-Benutzer und die WireGuard-Gruppe gesetzt

### Sichere Dateisystem-Operationen

- Verwendung von temporären Dateien und atomaren Operationen, um Race Conditions zu vermeiden
- Sicheres Löschen von Dateien durch mehrfaches Überschreiben mit Zufallsdaten
- Prüfung und Korrektur von Dateiberechtigungen beim Lesen

### Sichere Prozessausführung

- Verwendung von `sudo` für Operationen, die Root-Rechte erfordern
- Fehlerbehandlung und Logging für alle Prozessaufrufe
- Fallback-Mechanismen für kritische Operationen

### Backup und Wiederherstellung

- Automatische Backups vor Konfigurationsänderungen
- Sichere Speicherung von Backups mit Zeitstempel
- Sichere Wiederherstellung mit Backup der aktuellen Konfiguration

## API-Endpunkte

Die folgenden API-Endpunkte wurden implementiert, um die sicheren Systemoperationen zu nutzen:

### Schlüsselgenerierung

- `POST /api/v1/system/keys/generate`: Generiert ein neues WireGuard-Schlüsselpaar

### Konfigurationsdatei-Erstellung

- `POST /api/v1/system/config/server`: Erstellt eine neue WireGuard-Serverkonfigurationsdatei
- `POST /api/v1/system/config/client`: Erstellt eine neue WireGuard-Clientkonfigurationsdatei

### WireGuard-Neustarts/Updates

- `POST /api/v1/system/wireguard/restart/{interface}`: Startet ein WireGuard-Interface neu

### Backup-Funktionalität

- `GET /api/v1/system/backups`: Listet alle verfügbaren Backups auf
- `POST /api/v1/system/backups/restore`: Stellt eine WireGuard-Konfiguration aus einem Backup wieder her
- `POST /api/v1/system/backups/create/{interface}`: Erstellt ein Backup der aktuellen WireGuard-Konfiguration

## Verwendung

### Initialisierung

```python
from app.utils.system_operations import SecureSystemOperations

# Initialisiere die sicheren Systemoperationen
system_ops = SecureSystemOperations(
    wireguard_dir="/etc/wireguard",
    backup_dir="/var/backups/wireguard",
    wireguard_user="root",
    wireguard_group="root"
)
```

### Schlüsselgenerierung

```python
# Generiere einen privaten Schlüssel
private_key = await system_ops.generate_private_key()

# Leite den öffentlichen Schlüssel ab
public_key = await system_ops.derive_public_key(private_key)

# Generiere einen Preshared-Key
psk = await system_ops.generate_preshared_key()

# Speichere die Schlüssel
private_key_path = await system_ops.save_key(private_key, "server_private.key", is_private=True)
public_key_path = await system_ops.save_key(public_key, "server_public.key", is_private=False)
psk_path = await system_ops.save_key(psk, "peer1_psk.key", is_private=True)
```

### Konfigurationsdatei-Erstellung

```python
# Erstelle eine Server-Konfiguration
server_config_path = await system_ops.create_server_config(
    interface="wg0",
    private_key=private_key,
    address=["10.0.0.1/24"],
    listen_port=51820,
    peers=[
        {
            "public_key": "Peer1PublicKey",
            "allowed_ips": ["10.0.0.2/32"],
            "preshared_key": psk
        }
    ]
)

# Erstelle eine Client-Konfiguration
client_config_path = await system_ops.create_client_config(
    client_name="peer1",
    client_private_key="ClientPrivateKey",
    client_address=["10.0.0.2/32"],
    server_public_key=public_key,
    server_endpoint="server.example.com:51820",
    allowed_ips=["0.0.0.0/0"],
    dns_servers=["1.1.1.1", "8.8.8.8"],
    preshared_key=psk
)
```

### WireGuard-Neustarts/Updates

```python
# Starte ein WireGuard-Interface neu
success = await system_ops.restart_wireguard("wg0")

# Aktualisiere die Konfiguration eines laufenden WireGuard-Interfaces
success = await system_ops.update_wireguard_config("wg0", server_config_path)
```

### Backup-Funktionalität

```python
# Erstelle ein Backup
backup_path = await system_ops.backup_config("wg0")

# Liste alle Backups auf
backups = await system_ops.list_backups()

# Stelle eine Konfiguration wieder her
success = await system_ops.restore_config(backup_path, "wg0")
```

### Sichere Dateisystem-Operationen

```python
# Schreibe eine Datei sicher
success = await system_ops.secure_write_file(
    file_path=Path("/etc/wireguard/test.txt"),
    content="Dies ist ein Test.",
    is_private=True
)

# Lese eine Datei sicher
content = await system_ops.secure_read_file(Path("/etc/wireguard/test.txt"))

# Lösche eine Datei sicher
success = await system_ops.secure_delete_file(Path("/etc/wireguard/test.txt"))
```

## Fehlerbehebung

### Berechtigungsprobleme

Wenn Berechtigungsprobleme auftreten, stellen Sie sicher, dass:

1. Die Anwendung mit ausreichenden Rechten ausgeführt wird
2. Der WireGuard-Benutzer und die WireGuard-Gruppe existieren
3. Die Verzeichnisse mit den richtigen Berechtigungen erstellt wurden

### WireGuard-Neustarts

Wenn Probleme beim Neustart von WireGuard auftreten, prüfen Sie:

1. Ob WireGuard korrekt installiert ist
2. Ob die Konfigurationsdatei gültig ist
3. Die Logs mit `journalctl -u wg-quick@wg0.service`

### Backup und Wiederherstellung

Wenn Probleme bei Backup oder Wiederherstellung auftreten, prüfen Sie:

1. Ob die Backup-Verzeichnisse existieren und die richtigen Berechtigungen haben
2. Ob die Backup-Dateien gültig sind
3. Die Logs der Anwendung für detaillierte Fehlermeldungen 