from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime
import psutil

from app.models.client import Client
from app.schemas.client import ClientCreate, SystemStatus

class ClientService:
    def __init__(self, db: Session):
        self.db = db

    def get_clients(self, skip: int = 0, limit: int = 100):
        return self.db.query(Client).offset(skip).limit(limit).all()

    def get_total_clients(self) -> int:
        return self.db.query(Client).count()

    def get_client(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def create_client(self, client: ClientCreate):
        db_client = Client(
            name=client.name,
            public_key=client.public_key,
            allowed_ips=client.allowed_ips,
            email=client.email,
            description=client.description,
            is_active=True,
            created_at=datetime.utcnow()
        )
        self.db.add(db_client)
        self.db.commit()
        self.db.refresh(db_client)
        return db_client

    def delete_client(self, client_id: int):
        client = self.get_client(client_id)
        if client:
            self.db.delete(client)
            self.db.commit()

    def get_system_status(self) -> SystemStatus:
        total_clients = self.get_total_clients()
        active_clients = self.db.query(Client).filter(Client.is_active == True).count()
        
        # Aggregierte Transferstatistiken
        transfer_stats = self.db.query(
            func.coalesce(func.sum(Client.transfer_rx), 0).label('total_rx'),
            func.coalesce(func.sum(Client.transfer_tx), 0).label('total_tx')
        ).first()

        return SystemStatus(
            total_clients=total_clients,
            active_clients=active_clients,
            total_transfer_rx=transfer_stats.total_rx,
            total_transfer_tx=transfer_stats.total_tx,
            server_uptime=psutil.boot_time(),
            last_updated=datetime.utcnow()
        ) 