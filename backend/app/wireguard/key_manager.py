import os
from pathlib import Path
from typing import Tuple
import base64
import secrets
import subprocess
from dataclasses import dataclass

@dataclass
class KeyPair:
    private_key: str
    public_key: str

class WireGuardKeyManager:
    def __init__(self, key_dir: str = "/etc/wireguard"):
        self.key_dir = Path(key_dir)
        
    def _ensure_dir_exists(self):
        """Stellt sicher, dass das Schlüsselverzeichnis existiert und die richtigen Berechtigungen hat."""
        if not self.key_dir.exists():
            self.key_dir.mkdir(mode=0o700, parents=True)
        else:
            self.key_dir.chmod(0o700)

    def generate_keypair(self) -> KeyPair:
        """Generiert ein neues WireGuard-Schlüsselpaar."""
        private_key = base64.b64encode(secrets.token_bytes(32)).decode('ascii')
        
        # Generiere den öffentlichen Schlüssel mit wg pubkey
        try:
            process = subprocess.Popen(
                ['wg', 'pubkey'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            public_key, stderr = process.communicate(input=private_key.encode())
            
            if process.returncode != 0:
                raise RuntimeError(f"Fehler beim Generieren des öffentlichen Schlüssels: {stderr.decode()}")
            
            return KeyPair(
                private_key=private_key,
                public_key=public_key.decode().strip()
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Fehler beim Ausführen von wg pubkey: {e}")

    def save_keypair(self, name: str, keypair: KeyPair) -> Tuple[Path, Path]:
        """Speichert ein Schlüsselpaar sicher auf der Festplatte."""
        self._ensure_dir_exists()
        
        private_key_path = self.key_dir / f"{name}.key"
        public_key_path = self.key_dir / f"{name}.pub"
        
        # Speichere den privaten Schlüssel mit strengen Berechtigungen
        private_key_path.write_text(keypair.private_key)
        private_key_path.chmod(0o600)
        
        # Speichere den öffentlichen Schlüssel
        public_key_path.write_text(keypair.public_key)
        public_key_path.chmod(0o644)
        
        return private_key_path, public_key_path

    def load_keypair(self, name: str) -> KeyPair:
        """Lädt ein gespeichertes Schlüsselpaar."""
        private_key_path = self.key_dir / f"{name}.key"
        public_key_path = self.key_dir / f"{name}.pub"
        
        try:
            private_key = private_key_path.read_text().strip()
            public_key = public_key_path.read_text().strip()
            
            return KeyPair(private_key=private_key, public_key=public_key)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schlüsseldateien für {name} nicht gefunden")
        except PermissionError:
            raise PermissionError(f"Keine Berechtigung zum Lesen der Schlüsseldateien für {name}")

    def delete_keypair(self, name: str):
        """Löscht ein gespeichertes Schlüsselpaar sicher."""
        private_key_path = self.key_dir / f"{name}.key"
        public_key_path = self.key_dir / f"{name}.pub"
        
        # Überschreibe die Dateien vor dem Löschen
        if private_key_path.exists():
            private_key_path.write_bytes(secrets.token_bytes(32))
            private_key_path.unlink()
            
        if public_key_path.exists():
            public_key_path.unlink() 