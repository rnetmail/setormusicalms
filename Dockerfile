# Estágio 1: Builder - Compila o projeto Vite
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Runner - Serve os arquivos estáticos com Nginx
FROM nginx:stable-alpine

# Copia os arquivos compilados da pasta 'dist'
COPY --from=builder /app/dist /usr/share/nginx/html

# Copia a nossa configuração customizada do Nginx para dentro da imagem
# Isso sobrescreve a configuração padrão do Nginx
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
