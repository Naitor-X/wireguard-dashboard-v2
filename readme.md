# WireGuard Dashboard - Dokumentation

## Aktueller Entwicklungsstatus

Das WireGuard Dashboard ist ein Projekt zur Überwachung und Verwaltung von WireGuard VPN-Verbindungen. Es besteht aus einem Backend (FastAPI) und einem Frontend (React mit TypeScript), die über Docker containerisiert werden.

## Implementierte Features

### Backend (FastAPI)
1. **WireGuard-Monitoring**:
   - Automatische Überwachung des WireGuard-Interfaces (wg0)
   - Statusabfrage über API-Endpunkt
   - Regelmäßige Statusaktualisierung im Hintergrund

2. **Datenbank-Integration**:
   - PostgreSQL-Datenbank für Konfigurationsdaten
   - SQLAlchemy ORM für Datenbankzugriff
   - Alembic für Datenbankmigrationen

3. **API-Endpunkte**:
   - `/api/v1/health`: Gesundheitscheck
   - `/api/v1/wireguard/status`: WireGuard-Statusabfrage
   
   **Client-Management API**:
   - `GET /api/clients`: Liste aller Clients mit Pagination und Status
   - `GET /api/client/{id}`: Detail-Informationen eines Clients
   - `POST /api/client`: Neue Client-Konfiguration erstellen
   - `DELETE /api/client/{id}`: Client löschen
   - `GET /api/status`: System-Status und Statistiken

4. **Sichere Systemoperationen**:
   - Schlüsselgenerierung
   - Konfigurationsdatei-Erstellung
   - Sichere Dateisystem-Operationen
   - WireGuard-Neustarts/Updates
   - Backup-Funktionalität

### Frontend (React/TypeScript)
1. **Benutzeroberfläche**:
   - Material-UI als UI-Framework
   - Responsive Design

2. **Funktionen**:
   - Dashboard zur Anzeige des WireGuard-Status
   - React Query für API-Abfragen und Caching

3. **Komponenten**:
   - Layout-Komponenten für die Anwendungsstruktur
   - Feedback-Komponenten für Benachrichtigungen und Fehlerzustände
   - UI-Komponenten für einheitliches Design

## Entfernte Features

Die folgenden Features wurden aus dem Projekt entfernt:

1. **Authentifizierung**:
   - JWT-basierte Authentifizierung
   - Login-Endpunkt
   - Benutzermodell mit Rollen und Berechtigungen
   - Geschützte Routen im Frontend

## Projektstruktur

### Backend

```
backend/
├── app/                      # Hauptanwendungsverzeichnis
│   ├── api/                  # API-Definitionen
│   │   ├── endpoints/        # API-Endpunkte
│   │   │   └── clients.py    # Client-Management-Endpunkte
│   │   └── v1/               # API Version 1
│   │       ├── endpoints/    # API-Endpunkte
│   │       │   ├── health.py # Gesundheitscheck
│   │       │   ├── system_operations.py # Systemoperationen
│   │       │   └── wireguard.py # WireGuard-Endpunkte
│   │       └── api.py        # API-Router
│   ├── core/                 # Kernfunktionalität
│   ├── db/                   # Datenbankzugriff
│   ├── docs/                 # Dokumentation
│   ├── models/               # Datenbankmodelle
│   ├── schemas/              # Pydantic-Schemas
│   ├── services/             # Dienste
│   ├── utils/                # Hilfsfunktionen
│   ├── wireguard/            # WireGuard-spezifische Funktionen
│   └── main.py               # Hauptanwendungsdatei
├── Dockerfile                # Docker-Konfiguration
└── requirements.txt          # Python-Abhängigkeiten
```

### Frontend

```
frontend/
├── src/                      # Quellcode
│   ├── api/                  # API-Client
│   ├── components/           # Wiederverwendbare Komponenten
│   │   ├── common/           # Allgemeine Komponenten
│   │   ├── feedback/         # Feedback-Komponenten
│   │   ├── layout/           # Layout-Komponenten
│   │   │   └── MainLayout.tsx # Hauptlayout
│   │   └── ui/               # UI-Komponenten
│   ├── features/             # Feature-Module
│   ├── hooks/                # Benutzerdefinierte React-Hooks
│   ├── pages/                # Seitenkomponenten
│   │   ├── Dashboard.tsx     # Dashboard-Seite
│   │   └── NotFound.tsx      # 404-Seite
│   ├── services/             # Dienste
│   ├── store/                # State-Management
│   ├── styles/               # Styling
│   ├── types/                # TypeScript-Typdefinitionen
│   ├── utils/                # Hilfsfunktionen
│   ├── App.tsx               # Hauptanwendungskomponente
│   └── main.tsx              # Einstiegspunkt
├── Dockerfile                # Docker-Konfiguration
└── package.json              # NPM-Abhängigkeiten
```

## Technologiestack

### Backend
- **FastAPI**: Modernes, schnelles Web-Framework für Python
- **SQLAlchemy**: ORM für Datenbankzugriff
- **Pydantic**: Datenvalidierung und -serialisierung
- **PostgreSQL**: Relationale Datenbank

### Frontend
- **React**: JavaScript-Bibliothek für Benutzeroberflächen
- **TypeScript**: Typisiertes JavaScript
- **Material-UI**: UI-Komponentenbibliothek
- **React Router**: Routing-Bibliothek
- **React Query**: Datenabfrage und -caching
- **Axios**: HTTP-Client

### Infrastruktur
- **Docker**: Containerisierung
- **Docker Compose**: Multi-Container-Orchestrierung

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

## API-Dokumentation

### Client-Management API

#### GET /api/clients
Liefert eine Liste aller WireGuard-Clients mit Pagination.

**Parameter:**
- `skip` (optional): Anzahl der zu überspringenden Einträge (Standard: 0)
- `limit` (optional): Maximale Anzahl der zurückzugebenden Einträge (Standard: 100)

**Response:**
```json
{
    "clients": [
        {
            "id": 1,
            "name": "Client-Name",
            "public_key": "public_key_string",
            "allowed_ips": ["10.0.0.2/32"],
            "email": "optional@email.com",
            "description": "Optional description",
            "is_active": true,
            "created_at": "2024-03-16T14:30:00",
            "last_handshake": "2024-03-16T14:35:00",
            "transfer_rx": 1024,
            "transfer_tx": 2048
        }
    ],
    "total": 10
}
```

#### GET /api/client/{id}
Liefert detaillierte Informationen zu einem spezifischen Client.

**Response:** Einzelnes Client-Objekt (siehe oben)

#### POST /api/client
Erstellt einen neuen WireGuard-Client.

**Request Body:**
```json
{
    "name": "Neuer Client",
    "public_key": "client_public_key",
    "allowed_ips": ["10.0.0.2/32"],
    "email": "optional@email.com",
    "description": "Optional description"
}
```

#### DELETE /api/client/{id}
Löscht einen bestehenden Client.

#### GET /api/status
Liefert System-Status und Statistiken.

**Response:**
```json
{
    "total_clients": 10,
    "active_clients": 8,
    "total_transfer_rx": 1048576,
    "total_transfer_tx": 2097152,
    "server_uptime": 86400.0,
    "last_updated": "2024-03-16T14:30:00"
}
```

### System-Operationen API

- `POST /api/v1/system/keys/generate`: Generiert ein neues WireGuard-Schlüsselpaar
- `POST /api/v1/system/config/server`: Erstellt eine neue WireGuard-Serverkonfigurationsdatei
- `POST /api/v1/system/config/client`: Erstellt eine neue WireGuard-Clientkonfigurationsdatei
- `POST /api/v1/system/wireguard/restart/{interface}`: Startet ein WireGuard-Interface neu
- `GET /api/v1/system/backups`: Listet alle verfügbaren Backups auf
- `POST /api/v1/system/backups/restore`: Stellt eine WireGuard-Konfiguration aus einem Backup wieder her
- `POST /api/v1/system/backups/create/{interface}`: Erstellt ein Backup der aktuellen WireGuard-Konfiguration

## Installation und Ausführung

### Voraussetzungen
- Docker und Docker Compose
- WireGuard-Installation auf dem Host-System

### Ausführung
1. Repository klonen
2. `docker-compose up -d` ausführen
3. Frontend unter http://localhost:3000 aufrufen
4. Backend-API unter http://localhost:8000 verfügbar

## Aktueller Status und nächste Schritte

Das Projekt befindet sich in der Entwicklungsphase mit grundlegenden Funktionen:
- WireGuard-Statusabfrage ist funktionsfähig
- Client-Management ist implementiert
- Grundlegende UI ist vorhanden

Mögliche nächste Schritte:
1. Erweiterung des Dashboards mit detaillierten Statistiken
2. Verbesserung der Benutzeroberfläche
3. Implementierung von Benachrichtigungen bei Verbindungsproblemen
4. Hinzufügen von Benutzerauthentifizierung (optional)
5. Verbesserung der Sicherheit und Zugriffskontrollen
