FROM python:3.12-slim

# Installiere WireGuard-Tools und andere Abhängigkeiten
RUN apt-get update && \
    apt-get install -y wireguard-tools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Installiere das Backend-Paket
RUN pip install -e .

# Setze Berechtigungen für WireGuard-Verzeichnis
RUN mkdir -p /etc/wireguard && \
    chmod 750 /etc/wireguard && \
    chown root:root /etc/wireguard

# Wir verwenden den root-Benutzer für WireGuard-Zugriff
USER root

# Definiere Volume-Mountpoints explizit
VOLUME ["/app", "/etc/wireguard"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 