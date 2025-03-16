from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

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