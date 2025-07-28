# Estágio 1: Builder - Compila o projeto Vite
FROM node:20-alpine AS builder

WORKDIR /app

# Copia os arquivos de manifesto de pacote
COPY package.json ./
COPY package-lock.json ./

# Instala as dependências
RUN npm install

# Copia o resto do código-fonte
COPY . .

# Executa o build de produção (vite build)
RUN npm run build

# Estágio 2: Runner - Serve os arquivos estáticos com Nginx
FROM nginx:stable-alpine

# Copia os arquivos compilados da pasta 'dist' do estágio anterior
# para o diretório padrão do Nginx que serve HTML.
COPY --from=builder /app/dist /usr/share/nginx/html

# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80

# O comando padrão da imagem do Nginx já inicia o servidor,
# então não precisamos de um CMD.
