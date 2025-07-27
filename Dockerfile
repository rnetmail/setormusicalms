# Dockerfile
# Versão 117 - FINAL PARA O FRONTEND (React + Node.js)

# --- Estágio 1: Build da Aplicação React ---
FROM node:18-alpine AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Estágio 2: Servidor de Produção ---
FROM node:18-alpine

WORKDIR /app

# Instala o 'serve' para servir os arquivos estáticos
RUN npm install -g serve

# Copia os arquivos estáticos do build
COPY --from=build-stage /app/dist .

# Expõe a porta 8001, que o Nginx da VPS espera
EXPOSE 8001

# Executa o servidor na porta 8001
CMD ["serve", "-s", ".", "-l", "8001"]
