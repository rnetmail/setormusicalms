# nginx-proxy.Dockerfile
# Versão 01 - 29/07/2025 05:30 - Dockerfile para o serviço de proxy

FROM nginx:stable-alpine

# Copia o arquivo de configuração do proxy para o local correto dentro do contêiner
COPY nginx-proxy.conf /etc/nginx/conf.d/default.conf
