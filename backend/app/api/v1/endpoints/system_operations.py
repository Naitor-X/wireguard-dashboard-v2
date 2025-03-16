from fastapi import APIRouter, HTTPException, BackgroundTasks, Path, Query, Body
from typing import List, Dict, Any, Optional
from pathlib import Path as PathLib
import logging
from datetime import datetime

from app.utils.system_operations import SecureSystemOperations
from app.schemas.wireguard import (
    WireGuardKeyResponse,
    WireGuardConfigRequest,
    WireGuardConfigResponse,
    WireGuardBackupResponse,
    WireGuardRestoreRequest,
    SystemOperationResponse
)

# Logger konfigurieren
logger = logging.getLogger(__name__)

# Router erstellen
router = APIRouter()

# Initialisiere die sicheren Systemoperationen
system_ops = SecureSystemOperations()

@router.post("/keys/generate", response_model=WireGuardKeyResponse, status_code=201)
async def generate_keys(
    background_tasks: BackgroundTasks,
):
    """
    Generiert ein neues WireGuard-Schlüsselpaar (privater und öffentlicher Schlüssel).
    Nur für Administratoren verfügbar.
    """
    try:
        # Generiere einen privaten Schlüssel
        private_key = await system_ops.generate_private_key()
        
        # Leite den öffentlichen Schlüssel ab
        public_key = await system_ops.derive_public_key(private_key)
        
        # Generiere einen Preshared-Key
        preshared_key = await system_ops.generate_preshared_key()
        
        # Speichere die Schlüssel im Hintergrund
        background_tasks.add_task(system_ops.save_key, private_key, "server_private.key", True)
        background_tasks.add_task(system_ops.save_key, public_key, "server_public.key", False)
        
        return {
            "private_key": private_key,
            "public_key": public_key,
            "preshared_key": preshared_key,
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Fehler bei der Schlüsselgenerierung: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Schlüsselgenerierung: {str(e)}"
        )

@router.post("/config/server", response_model=WireGuardConfigResponse, status_code=201)
async def create_server_config(
    config_request: WireGuardConfigRequest,
    background_tasks: BackgroundTasks,
):
    """
    Erstellt eine neue WireGuard-Serverkonfigurationsdatei.
    Nur für Administratoren verfügbar.
    """
    try:
        # Erstelle die Serverkonfiguration
        config_path = await system_ops.create_server_config(
            interface=config_request.interface,
            private_key=config_request.private_key,
            address=config_request.address,
            listen_port=config_request.listen_port,
            peers=config_request.peers
        )
        
        # Erstelle ein Backup der vorherigen Konfiguration im Hintergrund
        background_tasks.add_task(system_ops.backup_config, config_request.interface)
        
        # Aktualisiere die WireGuard-Konfiguration im Hintergrund
        background_tasks.add_task(
            system_ops.update_wireguard_config,
            config_request.interface,
            config_path
        )
        
        return {
            "interface": config_request.interface,
            "config_path": str(config_path),
            "created_at": datetime.now().isoformat(),
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Fehler bei der Serverkonfigurationserstellung: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Serverkonfigurationserstellung: {str(e)}"
        )

@router.post("/config/client", response_model=WireGuardConfigResponse, status_code=201)
async def create_client_config(
    client_name: str = Query(..., description="Name des Clients"),
    client_private_key: str = Body(..., description="Privater Schlüssel des Clients"),
    client_address: List[str] = Body(..., description="IP-Adressen des Clients"),
    server_public_key: str = Body(..., description="Öffentlicher Schlüssel des Servers"),
    server_endpoint: str = Body(..., description="Endpunkt des Servers (IP:Port)"),
    allowed_ips: List[str] = Body(..., description="Erlaubte IPs für den Client"),
    dns_servers: Optional[List[str]] = Body(None, description="DNS-Server für den Client"),
    preshared_key: Optional[str] = Body(None, description="Preshared-Key für zusätzliche Sicherheit"),
    persistent_keepalive: Optional[int] = Body(25, description="Keepalive-Wert in Sekunden"),
):
    """
    Erstellt eine neue WireGuard-Clientkonfigurationsdatei.
    Nur für Administratoren verfügbar.
    """
    try:
        # Erstelle die Clientkonfiguration
        config_path = await system_ops.create_client_config(
            client_name=client_name,
            client_private_key=client_private_key,
            client_address=client_address,
            server_public_key=server_public_key,
            server_endpoint=server_endpoint,
            allowed_ips=allowed_ips,
            dns_servers=dns_servers,
            preshared_key=preshared_key,
            persistent_keepalive=persistent_keepalive
        )
        
        return {
            "interface": client_name,
            "config_path": str(config_path),
            "created_at": datetime.now().isoformat(),
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Fehler bei der Clientkonfigurationserstellung: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Clientkonfigurationserstellung: {str(e)}"
        )

@router.post("/wireguard/restart/{interface}", response_model=SystemOperationResponse)
async def restart_wireguard_interface(
    interface: str = Path(..., description="Name des WireGuard-Interfaces"),
):
    """
    Startet ein WireGuard-Interface neu.
    Nur für Administratoren verfügbar.
    """
    try:
        # Starte das WireGuard-Interface neu
        success = await system_ops.restart_wireguard(interface)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Fehler beim Neustart des WireGuard-Interfaces {interface}"
            )
        
        return {
            "operation": "restart",
            "interface": interface,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fehler beim Neustart des WireGuard-Interfaces: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Neustart des WireGuard-Interfaces: {str(e)}"
        )

@router.get("/backups", response_model=List[WireGuardBackupResponse])
async def list_backups(
    interface: Optional[str] = Query(None, description="Optionaler Name des WireGuard-Interfaces"),
):
    """
    Listet alle verfügbaren Backups auf.
    Nur für Administratoren verfügbar.
    """
    try:
        # Liste alle Backups auf
        backups = await system_ops.list_backups(interface)
        
        return backups
    except Exception as e:
        logger.error(f"Fehler beim Auflisten der Backups: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Auflisten der Backups: {str(e)}"
        )

@router.post("/backups/restore", response_model=SystemOperationResponse)
async def restore_backup(
    restore_request: WireGuardRestoreRequest,
):
    """
    Stellt eine WireGuard-Konfiguration aus einem Backup wieder her.
    Nur für Administratoren verfügbar.
    """
    try:
        # Stelle die Konfiguration wieder her
        success = await system_ops.restore_config(
            PathLib(restore_request.backup_path),
            restore_request.interface
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Fehler bei der Wiederherstellung der Konfiguration für {restore_request.interface}"
            )
        
        return {
            "operation": "restore",
            "interface": restore_request.interface,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fehler bei der Wiederherstellung der Konfiguration: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler bei der Wiederherstellung der Konfiguration: {str(e)}"
        )

@router.post("/backups/create/{interface}", response_model=WireGuardBackupResponse)
async def create_backup(
    interface: str = Path(..., description="Name des WireGuard-Interfaces"),
):
    """
    Erstellt ein Backup der aktuellen WireGuard-Konfiguration.
    Nur für Administratoren verfügbar.
    """
    try:
        # Erstelle ein Backup
        backup_path = await system_ops.backup_config(interface)
        
        if not backup_path:
            raise HTTPException(
                status_code=500,
                detail=f"Fehler beim Erstellen des Backups für {interface}"
            )
        
        # Erstelle die Antwort
        timestamp = datetime.now()
        
        return {
            "interface": interface,
            "path": str(backup_path),
            "timestamp": timestamp.isoformat(),
            "size": backup_path.stat().st_size
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fehler beim Erstellen des Backups: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Erstellen des Backups: {str(e)}"
        ) 