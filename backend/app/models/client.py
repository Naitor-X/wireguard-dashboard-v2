from sqlalchemy import Column, Integer, String, Boolean, DateTime, ARRAY
from sqlalchemy.sql import func
from app.db.base_class import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    public_key = Column(String(44), unique=True, nullable=False)
    allowed_ips = Column(ARRAY(String), nullable=False)
    email = Column(String(255))
    description = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_handshake = Column(DateTime(timezone=True))
    transfer_rx = Column(Integer, default=0)
    transfer_tx = Column(Integer, default=0) 