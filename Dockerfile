# /Dockerfile
# Versão 01 25/07/2025 17:21

# --- Estágio 1: Build da Aplicação React ---
FROM node:18-alpine AS build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Estágio 2: Servidor de Produção Nginx ---
FROM nginx:stable-alpine

# Copia os ficheiros estáticos gerados no estágio anterior
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copia o nosso ficheiro de configuração personalizado do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
