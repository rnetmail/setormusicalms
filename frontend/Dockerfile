# Dockerfile - Versão Final e Corrigida

# Estágio 1: Builder - Instala dependências e compila o projeto Vite
FROM node:20-alpine AS builder

WORKDIR /app

# 1. Copia TODOS os arquivos do projeto primeiro, incluindo o package.json mais recente.
COPY . .

# 2. AGORA executa o npm install. Ele lerá o package.json atualizado
#    e instalará TODAS as dependências, incluindo o @mui/material.
RUN npm install

# 3. Executa o build de produção. Agora o @mui/material existe e o build funcionará.
RUN npm run build

# Estágio 2: Runner - Serve os arquivos estáticos com Nginx
FROM nginx:stable-alpine

# Copia os arquivos compilados da pasta 'dist' do estágio anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Copia a configuração customizada do Nginx para lidar com a SPA
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
