# Dockerfile (na raiz do projeto)

# --- Estágio de Build ---
# Usa uma imagem Node.js para instalar as dependências e construir o projeto
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json ./
# Descomente a linha abaixo se tiver um package-lock.json
# COPY package-lock.json ./

RUN npm install

COPY . .

# O comando 'npm run build' cria a pasta 'dist' com os ficheiros otimizados
RUN npm run build

# --- Estágio de Produção ---
# Usa uma imagem Nginx super leve para servir os ficheiros
FROM nginx:stable-alpine

# Copia os ficheiros construídos do estágio anterior para a pasta pública do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia o nosso ficheiro de configuração customizado para o Nginx (próximo passo)
COPY nginx.conf /etc/nginx/conf.d

# O Nginx dentro do contentor vai correr na porta 80
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
