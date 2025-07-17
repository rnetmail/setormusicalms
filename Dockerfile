# Dockerfile
# Versão 32 17/07/2025 22:31

# --- Estágio 1: Build da Aplicação React ---
# Usamos uma imagem oficial do Node.js como base para o build.
# O alias 'build-stage' nos permite referenciar este estágio depois.
FROM node:18-alpine AS build-stage

# Define o diretório de trabalho dentro do contentor.
WORKDIR /app

# Copia os ficheiros de definição de pacotes.
COPY package*.json ./

# Instala as dependências do projeto.
RUN npm install

# Copia todo o resto do código da aplicação para o contentor.
COPY . .

# Executa o comando de build para gerar os ficheiros estáticos de produção.
RUN npm run build


# --- Estágio 2: Configuração do Servidor Nginx ---
# Usamos uma imagem oficial e leve do Nginx para servir os ficheiros.
FROM nginx:stable-alpine

# Copia os ficheiros estáticos gerados no estágio anterior para a pasta
# padrão do Nginx que serve conteúdo web.
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copia o seu ficheiro de configuração personalizado do Nginx para dentro
# do contentor, substituindo a configuração padrão.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expõe a porta 80 para permitir o acesso ao Nginx.
EXPOSE 80

# O comando padrão para iniciar o Nginx quando o contentor arrancar.
CMD ["nginx", "-g", "daemon off;"]
