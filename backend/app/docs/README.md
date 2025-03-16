# WireGuard-Dashboard Dokumentation

## Sichere Systemoperationen

Die folgenden sicheren Systemoperationen wurden implementiert:

### 1. Schlüsselgenerierung

- Sichere Generierung von privaten, öffentlichen und Preshared-Keys
- Verwendung von WireGuard-Kommandozeilentools mit Fallback auf kryptografisch sichere Python-Funktionen
- Sichere Speicherung von Schlüsseln mit minimalen Berechtigungen

### 2. Konfigurationsdatei-Erstellung

- Sichere Erstellung von Server- und Client-Konfigurationsdateien
- Verwendung von temporären Dateien und atomaren Operationen
- Sichere Berechtigungen für Konfigurationsdateien

### 3. Sichere Dateisystem-Operationen

- Sichere Lese-, Schreib- und Löschoperationen
- Sicheres Löschen durch mehrfaches Überschreiben mit Zufallsdaten
- Prüfung und Korrektur von Dateiberechtigungen

### 4. WireGuard-Neustarts/Updates

- Sichere Neustarts von WireGuard-Interfaces
- Sichere Updates von WireGuard-Konfigurationen
- Automatische Backups vor Konfigurationsänderungen

### 5. Backup-Funktionalität

- Erstellung, Auflistung und Wiederherstellung von Backups
- Sichere Speicherung von Backups mit Zeitstempel
- Sichere Wiederherstellung mit Backup der aktuellen Konfiguration

## API-Endpunkte

Die folgenden API-Endpunkte wurden implementiert, um die sicheren Systemoperationen zu nutzen:

- `POST /api/v1/system/keys/generate`: Generiert ein neues WireGuard-Schlüsselpaar
- `POST /api/v1/system/config/server`: Erstellt eine neue WireGuard-Serverkonfigurationsdatei
- `POST /api/v1/system/config/client`: Erstellt eine neue WireGuard-Clientkonfigurationsdatei
- `POST /api/v1/system/wireguard/restart/{interface}`: Startet ein WireGuard-Interface neu
- `GET /api/v1/system/backups`: Listet alle verfügbaren Backups auf
- `POST /api/v1/system/backups/restore`: Stellt eine WireGuard-Konfiguration aus einem Backup wieder her
- `POST /api/v1/system/backups/create/{interface}`: Erstellt ein Backup der aktuellen WireGuard-Konfiguration

## Sicherheitsmaßnahmen

Die folgenden Sicherheitsmaßnahmen wurden implementiert:

- Minimale Berechtigungen für Dateien und Verzeichnisse
- Sichere Prozessausführung mit `sudo`
- Fehlerbehandlung und Logging für alle Operationen
- Fallback-Mechanismen für kritische Operationen
- Verwendung von temporären Dateien und atomaren Operationen

Weitere Details finden Sie in der [Dokumentation der sicheren Systemoperationen](system_operations.md). 