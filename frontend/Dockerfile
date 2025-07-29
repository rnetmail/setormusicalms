# frontend/Dockerfile - Versão Final para servir arquivos estáticos (sem build)

# Usa uma imagem Nginx leve
FROM nginx:stable-alpine

# Copia TODOS os arquivos do seu projeto frontend para a pasta que o Nginx serve
# Isso inclui index.html, index.tsx, pages/, components/, etc.
COPY . /usr/share/nginx/html

# Copia a configuração do Nginx para lidar com o roteamento do React (SPA)
COPY nginx-frontend.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
