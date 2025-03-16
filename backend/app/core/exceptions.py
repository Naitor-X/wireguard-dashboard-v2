from fastapi import HTTPException, status

class WireGuardException(HTTPException):
    """Basis-Exception für WireGuard-spezifische Fehler"""
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Ein unerwarteter Fehler ist aufgetreten"
    ):
        super().__init__(status_code=status_code, detail=detail)

class AuthenticationError(WireGuardException):
    """Exception für Authentifizierungsfehler"""
    def __init__(self, detail: str = "Authentifizierung fehlgeschlagen"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class AuthorizationError(WireGuardException):
    """Exception für Autorisierungsfehler"""
    def __init__(self, detail: str = "Keine Berechtigung für diese Operation"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class ResourceNotFoundError(WireGuardException):
    """Exception für nicht gefundene Ressourcen"""
    def __init__(self, detail: str = "Ressource nicht gefunden"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        ) 