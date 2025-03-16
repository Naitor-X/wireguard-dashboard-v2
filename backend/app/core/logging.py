import sys
from loguru import logger
from .config import settings

# Logging-Konfiguration
def setup_logging():
    # Entferne Standard-Handler
    logger.remove()
    
    # Füge Console-Handler hinzu
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG" if settings.ENVIRONMENT == "development" else "INFO",
        colorize=True
    )
    
    # Füge File-Handler für Fehler hinzu
    logger.add(
        "logs/error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="ERROR",
        rotation="10 MB",
        retention="1 week"
    )

# Initialisiere Logging beim Import
setup_logging() 