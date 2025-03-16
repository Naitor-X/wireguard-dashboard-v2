from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import re
import os

@dataclass
class WireGuardPeer:
    public_key: str
    allowed_ips: List[str]
    endpoint: Optional[str] = None
    persistent_keepalive: Optional[int] = None

@dataclass
class WireGuardConfig:
    private_key: str
    address: List[str]
    listen_port: Optional[int]
    peers: List[WireGuardPeer]

class WireGuardConfigParser:
    def __init__(self, config_dir: str = "/etc/wireguard"):
        self.config_dir = Path(config_dir)
    
    def _read_config_file(self, filename: str) -> str:
        try:
            with open(self.config_dir / filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Konfigurationsdatei {filename} nicht gefunden")
        except PermissionError:
            raise PermissionError(f"Keine Berechtigung zum Lesen von {filename}")

    def _parse_section(self, section: str) -> Dict[str, str]:
        config = {}
        for line in section.strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
        return config

    def parse_config(self, filename: str) -> WireGuardConfig:
        content = self._read_config_file(filename)
        sections = re.split(r'\[(.+?)\]', content)[1:]
        
        if not sections or sections[0] != 'Interface':
            raise ValueError("Ungültiges WireGuard-Konfigurationsformat")

        # Parse Interface section
        interface_section = sections[1]  # Die Interface-Sektion ist der Text nach [Interface]
        interface_config = self._parse_section(interface_section)
        peers = []

        # Parse Interface section
        address = [addr.strip() for addr in interface_config.get('Address', '').split(',')]
        private_key = interface_config.get('PrivateKey', '').strip()
        listen_port = int(interface_config.get('ListenPort', 0)) if 'ListenPort' in interface_config else None

        # Parse Peer sections
        for i in range(2, len(sections), 2):
            if sections[i] == 'Peer':
                peer_config = self._parse_section(sections[i + 1])
                peers.append(WireGuardPeer(
                    public_key=peer_config.get('PublicKey', '').strip(),
                    allowed_ips=[ip.strip() for ip in peer_config.get('AllowedIPs', '').split(',')],
                    endpoint=peer_config.get('Endpoint'),
                    persistent_keepalive=int(peer_config.get('PersistentKeepalive', 0)) if 'PersistentKeepalive' in peer_config else None
                ))

        if not private_key:
            raise ValueError("Private Key fehlt in der Konfiguration")

        return WireGuardConfig(
            private_key=private_key,
            address=address,
            listen_port=listen_port,
            peers=peers
        ) 