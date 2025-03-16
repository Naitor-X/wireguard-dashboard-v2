from pydantic import BaseModel, IPvAnyAddress, constr
from typing import Optional, List
from datetime import datetime

class ClientBase(BaseModel):
    name: constr(min_length=1, max_length=64)
    public_key: constr(min_length=44, max_length=44)
    allowed_ips: List[str]
    email: Optional[str] = None
    description: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    is_active: bool
    created_at: datetime
    last_handshake: Optional[datetime]
    transfer_rx: Optional[int]
    transfer_tx: Optional[int]

    class Config:
        from_attributes = True

class ClientList(BaseModel):
    clients: List[ClientResponse]
    total: int

class SystemStatus(BaseModel):
    total_clients: int
    active_clients: int
    total_transfer_rx: int
    total_transfer_tx: int
    server_uptime: float
    last_updated: datetime 