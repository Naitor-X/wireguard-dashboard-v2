from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.core.config import settings
from app.core.logging import logger
from app.api.v1.api import router as api_v1_router
from app.db.session import engine
from app.db.session import SessionLocal
from app.api.v1.endpoints.wireguard import wireguard_monitor
from app.api.endpoints import clients

# Globale Variable für die Monitor-Task
monitor_task = None

def create_application() -> FastAPI:
    app = FastAPI(
        title="WireGuard Dashboard API",
        description="REST API für das WireGuard Dashboard",
        version="1.0.0"
    )

    # CORS-Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Router einbinden
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    app.include_router(clients.router, prefix="/api", tags=["clients"])

    @app.on_event("startup")
    async def startup_event():
        global monitor_task
        
        logger.info(f"Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode")
            
        # Starte den WireGuard-Monitor in einer Hintergrund-Task
        logger.info("Starte WireGuard-Monitor...")
        monitor_task = asyncio.create_task(wireguard_monitor.start())

    @app.on_event("shutdown")
    async def shutdown_event():
        global monitor_task
        
        logger.info(f"Shutting down {settings.PROJECT_NAME}")
        
        # Stoppe den WireGuard-Monitor
        wireguard_monitor.stop()
        
        # Warte auf das Ende der Monitor-Task
        if monitor_task:
            try:
                await asyncio.wait_for(monitor_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Timeout beim Warten auf das Ende des WireGuard-Monitors")

    return app

app = create_application() 