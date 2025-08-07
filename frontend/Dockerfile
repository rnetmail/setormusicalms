# frontend/Dockerfile - Versão Final para servir arquivos estáticos (sem build)
# Estágio 1: Build da aplicação Vue.js
FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Servir a aplicação com Nginx
FROM nginx:stable-alpine
# Copia os arquivos buildados do estágio anterior
COPY --from=builder /app/dist /usr/share/nginx/html
# Copia a configuração customizada do Nginx
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
