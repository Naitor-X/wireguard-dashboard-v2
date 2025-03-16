FROM node:18-bullseye as build

WORKDIR /app

COPY package*.json ./
COPY tsconfig*.json ./

# Installiere die Abhängigkeiten
RUN npm install

COPY . .

# Build für Produktion
RUN npm run build

# Produktions-Stage
FROM nginx:stable-alpine

# Kopiere die gebauten Dateien in das nginx-Verzeichnis
COPY --from=build /app/dist /usr/share/nginx/html

# Kopiere nginx-Konfiguration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

# Starte nginx mit Port 3000
CMD ["nginx", "-g", "daemon off;"] 