# Dockerfile
# Versão 33 22/07/2025 15:12

# --- Estágio 1: Build da Aplicação React ---
# Usamos uma imagem oficial do Node.js como base para o build.
FROM node:18-alpine AS build-stage

# Define o diretório de trabalho dentro do contentor.
WORKDIR /app

# Copia os ficheiros de definição de pacotes.
COPY package*.json ./

# Instala as dependências do projeto, incluindo o 'serve'.
RUN npm install

# Copia todo o resto do código da aplicação para o contentor.
COPY . .

# Executa o comando de build para gerar os ficheiros estáticos de produção.
RUN npm run build


# --- Estágio 2: Servidor de Produção Node.js ---
# Usamos uma imagem base do Node.js leve para produção.
FROM node:18-alpine

WORKDIR /app

# Copia as dependências de produção do estágio de build.
COPY --from=build-stage /app/package*.json ./
RUN npm install --omit=dev

# Copia os ficheiros estáticos gerados no estágio de build.
COPY --from=build-stage /app/dist ./dist

# Expõe a porta 3000, onde o servidor 'serve' irá rodar.
EXPOSE 3000

# O comando para iniciar o servidor 'serve' em produção.
CMD ["npm", "start"]
