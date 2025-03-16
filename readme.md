# WireGuard Dashboard - Dokumentation

## Aktueller Entwicklungsstatus

Das WireGuard Dashboard ist ein Projekt zur Überwachung und Verwaltung von WireGuard VPN-Verbindungen. Es besteht aus einem Backend (FastAPI) und einem Frontend (React mit TypeScript), die über Docker containerisiert werden.

## Implementierte Features

### Backend (FastAPI)
1. **Authentifizierung**: 
   - JWT-basierte Authentifizierung mit Login-Endpunkt
   - Benutzermodell mit Rollen und Berechtigungen

2. **WireGuard-Monitoring**:
   - Automatische Überwachung des WireGuard-Interfaces (wg0)
   - Statusabfrage über API-Endpunkt
   - Regelmäßige Statusaktualisierung im Hintergrund

3. **Datenbank-Integration**:
   - PostgreSQL-Datenbank für Benutzer und Konfigurationsdaten
   - SQLAlchemy ORM für Datenbankzugriff
   - Alembic für Datenbankmigrationen

4. **API-Endpunkte**:
   - `/api/v1/health`: Gesundheitscheck
   - `/api/v1/auth`: Authentifizierungsendpunkte (Login, etc.)
   - `/api/v1/wireguard/status`: WireGuard-Statusabfrage
   
   **Neue Client-Management API**:
   - `GET /api/clients`: Liste aller Clients mit Pagination und Status
   - `GET /api/client/{id}`: Detail-Informationen eines Clients
   - `POST /api/client`: Neue Client-Konfiguration erstellen
   - `DELETE /api/client/{id}`: Client löschen (mit Authentifizierung)
   - `GET /api/status`: System-Status und Statistiken

### Frontend (React/TypeScript)
1. **Benutzeroberfläche**:
   - Material-UI als UI-Framework
   - Responsive Design
   - Geschützte Routen mit Authentifizierung

2. **Funktionen**:
   - Login-Seite mit Formularvalidierung
   - Dashboard zur Anzeige des WireGuard-Status
   - React Query für API-Abfragen und Caching

3. **State Management**:
   - Redux für globalen Zustand
   - React Query für Server-State

## Projektstruktur

### Backend

```
backend/
├── app/                      # Hauptanwendungsverzeichnis
│   ├── api/                  # API-Definitionen
│   │   └── v1/               # API Version 1
│   │       ├── endpoints/    # API-Endpunkte
│   │       │   ├── auth.py   # Authentifizierungsendpunkte
│   │       │   ├── health.py # Gesundheitscheck
│   │       │   └── wireguard.py # WireGuard-Endpunkte
│   │       └── api.py        # API-Router
│   ├── core/                 # Kernfunktionalität
│   ├── db/                   # Datenbankzugriff
│   ├── models/               # Datenbankmodelle
│   ├── schemas/              # Pydantic-Schemas
│   ├── services/             # Dienste
│   │   └── wireguard_monitor.py # WireGuard-Überwachung
│   ├── utils/                # Hilfsfunktionen
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
│   │   └── Layout.tsx        # Hauptlayout
│   ├── features/             # Feature-Module
│   ├── hooks/                # Benutzerdefinierte React-Hooks
│   ├── pages/                # Seitenkomponenten
│   │   ├── Dashboard.tsx     # Dashboard-Seite
│   │   ├── Login.tsx         # Login-Seite
│   │   └── NotFound.tsx      # 404-Seite
│   ├── services/             # Dienste
│   │   └── auth.ts           # Authentifizierungsdienst
│   ├── store/                # Redux-Store
│   ├── styles/               # Styling
│   │   └── theme.ts          # Material-UI-Theme
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
- **JWT**: Token-basierte Authentifizierung
- **PostgreSQL**: Relationale Datenbank

### Frontend
- **React**: JavaScript-Bibliothek für Benutzeroberflächen
- **TypeScript**: Typisiertes JavaScript
- **Material-UI**: UI-Komponentenbibliothek
- **React Router**: Routing-Bibliothek
- **React Query**: Datenabfrage und -caching
- **Redux Toolkit**: State-Management
- **Axios**: HTTP-Client

### Infrastruktur
- **Docker**: Containerisierung
- **Docker Compose**: Multi-Container-Orchestrierung

## Aktueller Status und nächste Schritte

Das Projekt befindet sich in der Entwicklungsphase mit grundlegenden Funktionen:
- Authentifizierung ist implementiert
- WireGuard-Statusabfrage ist funktionsfähig
- Grundlegende UI ist vorhanden

Mögliche nächste Schritte:
1. Implementierung von Benutzer- und Peer-Verwaltung
2. Erweiterung des Dashboards mit detaillierten Statistiken
3. Implementierung von Konfigurationsänderungen über die UI
4. Hinzufügen von Benachrichtigungen bei Verbindungsproblemen
5. Verbesserung der Sicherheit und Zugriffskontrollen

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

Diese Dokumentation bietet einen Überblick über den aktuellen Stand des WireGuard Dashboard-Projekts und seine Komponenten.
