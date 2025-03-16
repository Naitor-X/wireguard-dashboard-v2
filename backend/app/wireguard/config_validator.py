import ipaddress
from typing import List, Optional
import re
from dataclasses import dataclass

@dataclass
class ValidationError:
    field: str
    message: str

class WireGuardConfigValidator:
    @staticmethod
    def validate_key(key: str) -> List[ValidationError]:
        """Validiert einen WireGuard-Schlüssel."""
        errors = []
        if not key:
            errors.append(ValidationError("key", "Schlüssel darf nicht leer sein"))
        elif not re.match(r'^[A-Za-z0-9+/]{43}=$', key):
            errors.append(ValidationError("key", "Ungültiges Schlüsselformat"))
        return errors

    @staticmethod
    def validate_ip_addresses(addresses: List[str]) -> List[ValidationError]:
        """Validiert IP-Adressen und Subnetze."""
        errors = []
        if not addresses:
            errors.append(ValidationError("address", "Mindestens eine IP-Adresse erforderlich"))
        
        for addr in addresses:
            try:
                # Validiere IPv4 und IPv6 Adressen mit CIDR-Notation
                ipaddress.ip_network(addr.strip(), strict=False)
            except ValueError as e:
                errors.append(ValidationError("address", f"Ungültige IP-Adresse: {addr} - {str(e)}"))
        
        return errors

    @staticmethod
    def validate_port(port: Optional[int]) -> List[ValidationError]:
        """Validiert einen Port."""
        errors = []
        if port is not None:
            if not isinstance(port, int):
                errors.append(ValidationError("port", "Port muss eine Ganzzahl sein"))
            elif port < 1 or port > 65535:
                errors.append(ValidationError("port", "Port muss zwischen 1 und 65535 liegen"))
        return errors

    @staticmethod
    def validate_endpoint(endpoint: Optional[str]) -> List[ValidationError]:
        """Validiert einen Endpoint (Host:Port)."""
        errors = []
        if endpoint:
            parts = endpoint.split(':')
            if len(parts) != 2:
                errors.append(ValidationError("endpoint", "Endpoint muss im Format 'Host:Port' sein"))
            else:
                host, port = parts
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        errors.append(ValidationError("endpoint", "Port muss zwischen 1 und 65535 liegen"))
                except ValueError:
                    errors.append(ValidationError("endpoint", "Port muss eine Ganzzahl sein"))
                
                # Validiere Hostname/IP
                if not re.match(r'^[a-zA-Z0-9.-]+$', host):
                    try:
                        ipaddress.ip_address(host)
                    except ValueError:
                        errors.append(ValidationError("endpoint", "Ungültiger Hostname oder IP-Adresse"))
        
        return errors

    @staticmethod
    def validate_keepalive(keepalive: Optional[int]) -> List[ValidationError]:
        """Validiert den PersistentKeepalive-Wert."""
        errors = []
        if keepalive is not None:
            if not isinstance(keepalive, int):
                errors.append(ValidationError("keepalive", "PersistentKeepalive muss eine Ganzzahl sein"))
            elif keepalive < 0:
                errors.append(ValidationError("keepalive", "PersistentKeepalive muss positiv sein"))
        return errors

    def validate_peer(self, peer_config: dict) -> List[ValidationError]:
        """Validiert die Konfiguration eines Peers."""
        errors = []
        
        # Validiere erforderliche Felder
        if 'PublicKey' not in peer_config:
            errors.append(ValidationError("peer", "PublicKey ist erforderlich"))
        else:
            errors.extend(self.validate_key(peer_config['PublicKey']))
        
        if 'AllowedIPs' not in peer_config:
            errors.append(ValidationError("peer", "AllowedIPs ist erforderlich"))
        else:
            allowed_ips = [ip.strip() for ip in peer_config['AllowedIPs'].split(',')]
            errors.extend(self.validate_ip_addresses(allowed_ips))
        
        # Validiere optionale Felder
        if 'Endpoint' in peer_config:
            errors.extend(self.validate_endpoint(peer_config['Endpoint']))
        
        if 'PersistentKeepalive' in peer_config:
            try:
                keepalive = int(peer_config['PersistentKeepalive'])
                errors.extend(self.validate_keepalive(keepalive))
            except ValueError:
                errors.append(ValidationError("keepalive", "PersistentKeepalive muss eine Ganzzahl sein"))
        
        return errors

    def validate_interface(self, interface_config: dict) -> List[ValidationError]:
        """Validiert die Interface-Konfiguration."""
        errors = []
        
        # Validiere erforderliche Felder
        if 'PrivateKey' not in interface_config:
            errors.append(ValidationError("interface", "PrivateKey ist erforderlich"))
        else:
            errors.extend(self.validate_key(interface_config['PrivateKey']))
        
        if 'Address' not in interface_config:
            errors.append(ValidationError("interface", "Address ist erforderlich"))
        else:
            addresses = [addr.strip() for addr in interface_config['Address'].split(',')]
            errors.extend(self.validate_ip_addresses(addresses))
        
        # Validiere optionale Felder
        if 'ListenPort' in interface_config:
            try:
                port = int(interface_config['ListenPort'])
                errors.extend(self.validate_port(port))
            except ValueError:
                errors.append(ValidationError("port", "ListenPort muss eine Ganzzahl sein"))
        
        return errors 