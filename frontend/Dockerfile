FROM node:18-bullseye as build

WORKDIR /app

COPY package*.json ./
COPY tsconfig*.json ./

# Installiere die Abhängigkeiten
RUN npm install

COPY . .

# Build für Produktion mit --force Flag, um TypeScript-Fehler zu ignorieren
RUN npm run build -- --mode production --force

# Produktions-Stage
FROM nginx:stable-alpine

# Kopiere die gebauten Dateien in das nginx-Verzeichnis
COPY --from=build /app/dist /usr/share/nginx/html

# Kopiere nginx-Konfiguration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

# Starte nginx mit Port 3000
CMD ["nginx", "-g", "daemon off;"] 