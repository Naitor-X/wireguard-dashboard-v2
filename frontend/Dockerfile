FROM node:18-bullseye

WORKDIR /app

COPY package*.json ./
COPY tsconfig*.json ./

# Installiere die Abhängigkeiten
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"] 