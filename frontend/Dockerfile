# frontend/Dockerfile - Versão Final para servir arquivos estáticos (sem build)
# Estágio 1: Build da aplicação Vue.js
# /frontend/Dockerfile - Versão Otimizada
# Estágio 1: Build da aplicação com Vite

FROM node:20-alpine AS builder
WORKDIR /app

# 1. Copia apenas os arquivos de manifesto de dependência
COPY package.json package-lock.json ./

# 2. Instala as dependências. Esta camada será cacheada se os arquivos acima não mudarem.
RUN npm install

# 3. Copia todo o código-fonte do projeto
COPY . .

# 4. Executa o build de produção
RUN npm run build

# Estágio 2: Servir os arquivos estáticos com Nginx
FROM nginx:stable-alpine

# Copia os arquivos compilados da pasta 'dist' do estágio anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Copia a configuração customizada do Nginx
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

