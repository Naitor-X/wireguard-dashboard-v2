from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.client import ClientCreate, ClientResponse, ClientList, SystemStatus
from app.services.client import ClientService

router = APIRouter()

@router.get("/clients", response_model=ClientList)
def get_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Liste aller Clients mit Status"""
    clients = ClientService(db).get_clients(skip=skip, limit=limit)
    total = ClientService(db).get_total_clients()
    return ClientList(clients=clients, total=total)

@router.get("/client/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Detail-Informationen eines Clients"""
    client = ClientService(db).get_client(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client nicht gefunden"
        )
    return client

@router.post("/client", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    """Neue Client-Konfiguration erstellen"""
    return ClientService(db).create_client(client)

@router.delete("/client/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Client löschen"""
    client = ClientService(db).get_client(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client nicht gefunden"
        )
    ClientService(db).delete_client(client_id)

@router.get("/status", response_model=SystemStatus)
def get_system_status(
    db: Session = Depends(get_db)
):
    """System-Status und Statistiken abrufen"""
    return ClientService(db).get_system_status() 