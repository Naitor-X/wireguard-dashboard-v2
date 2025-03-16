from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class WireGuardKeyResponse(BaseModel):
    """Schema für die Antwort der Schlüsselgenerierung."""
    private_key: str = Field(..., description="Der generierte private Schlüssel")
    public_key: str = Field(..., description="Der abgeleitete öffentliche Schlüssel")
    preshared_key: str = Field(..., description="Der generierte Preshared-Key")
    created_at: str = Field(..., description="Zeitstempel der Erstellung")

class WireGuardPeerConfig(BaseModel):
    """Schema für die Konfiguration eines WireGuard-Peers."""
    public_key: str = Field(..., description="Der öffentliche Schlüssel des Peers")
    allowed_ips: List[str] = Field(..., description="Liste der erlaubten IPs für den Peer")
    preshared_key: Optional[str] = Field(None, description="Optionaler Preshared-Key für zusätzliche Sicherheit")
    endpoint: Optional[str] = Field(None, description="Optionaler Endpunkt des Peers (IP:Port)")
    persistent_keepalive: Optional[int] = Field(None, description="Optionaler Keepalive-Wert in Sekunden")

class WireGuardConfigRequest(BaseModel):
    """Schema für die Anfrage zur Erstellung einer WireGuard-Konfiguration."""
    interface: str = Field(..., description="Name des WireGuard-Interfaces (z.B. wg0)")
    private_key: str = Field(..., description="Der private Schlüssel des Servers")
    address: List[str] = Field(..., description="Liste der IP-Adressen für das Interface")
    listen_port: int = Field(..., description="Der Port, auf dem der Server lauscht")
    peers: List[Dict[str, Any]] = Field(..., description="Liste der Peer-Konfigurationen")

class WireGuardConfigResponse(BaseModel):
    """Schema für die Antwort der Konfigurationserstellung."""
    interface: str = Field(..., description="Name des WireGuard-Interfaces")
    config_path: str = Field(..., description="Pfad zur erstellten Konfigurationsdatei")
    created_at: str = Field(..., description="Zeitstempel der Erstellung")
    status: str = Field(..., description="Status der Konfigurationserstellung")

class WireGuardBackupResponse(BaseModel):
    """Schema für die Antwort der Backup-Auflistung."""
    interface: str = Field(..., description="Name des WireGuard-Interfaces")
    path: str = Field(..., description="Pfad zur Backup-Datei")
    timestamp: str = Field(..., description="Zeitstempel des Backups")
    size: int = Field(..., description="Größe der Backup-Datei in Bytes")

class WireGuardRestoreRequest(BaseModel):
    """Schema für die Anfrage zur Wiederherstellung einer Konfiguration."""
    interface: str = Field(..., description="Name des WireGuard-Interfaces")
    backup_path: str = Field(..., description="Pfad zur Backup-Datei")

class SystemOperationResponse(BaseModel):
    """Schema für die Antwort einer Systemoperation."""
    operation: str = Field(..., description="Art der Operation")
    interface: str = Field(..., description="Name des WireGuard-Interfaces")
    success: bool = Field(..., description="Ob die Operation erfolgreich war")
    timestamp: str = Field(..., description="Zeitstempel der Operation")

class WireGuardPeerStatus(BaseModel):
    """Schema für den Status eines WireGuard-Peers."""
    public_key: str = Field(..., description="Öffentlicher Schlüssel des Peers")
    endpoint: Optional[str] = Field(None, description="Endpunkt des Peers (IP:Port)")
    allowed_ips: List[str] = Field(..., description="Erlaubte IP-Adressen")
    latest_handshake: int = Field(0, description="Zeitstempel des letzten Handshakes")
    transfer_rx: int = Field(0, description="Empfangene Bytes")
    transfer_tx: int = Field(0, description="Gesendete Bytes")
    persistent_keepalive: Optional[str] = Field(None, description="Persistent Keepalive Intervall")
    online: bool = Field(False, description="Online-Status des Peers")
    last_activity: Optional[str] = Field(None, description="Zeitpunkt der letzten Aktivität")
    type: str = Field("unknown", description="Typ des Peers (admin, user, unknown)")

class WireGuardStatus(BaseModel):
    """Schema für den WireGuard-Status."""
    timestamp: str = Field(..., description="Zeitstempel der Statusabfrage")
    interface: str = Field(..., description="Name des WireGuard-Interfaces")
    public_key: Optional[str] = Field(None, description="Öffentlicher Schlüssel des Interfaces")
    listen_port: Optional[str] = Field(None, description="Port, auf dem das Interface lauscht")
    peers: List[WireGuardPeerStatus] = Field([], description="Liste der Peers") 