# Dockerfile
# Versão 113

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
RUN npm install -g serve
COPY --from=build-stage /app/dist .
# Expõe a porta 3000 interna
EXPOSE 3000
# Executa o servidor na porta 3000 interna
CMD ["serve", "-s", ".", "-l", "3000"]
