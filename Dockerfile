# Dockerfile
# Versão 34 - Corrigido e Validado em 22/07/2025

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

# Instala apenas o 'serve' como dependência global
RUN npm install -g serve

# Copia os arquivos estáticos do build
COPY --from=build-stage /app/dist .

# Expondo a porta padrão do 'serve'
EXPOSE 8001

# Executa o servidor serve na porta 8001
CMD ["serve", "-s", ".", "-l", "8001"]
