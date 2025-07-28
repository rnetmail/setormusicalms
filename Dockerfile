# Estágio 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copia apenas os arquivos de manifesto de pacote primeiro
# Isso aproveita o cache do Docker se as dependências não mudarem
COPY package.json ./
COPY package-lock.json ./

# Instala todas as dependências
RUN npm install

# Agora copia o resto dos arquivos do projeto
# Isso inclui /app, /pages, /public, next.config.mjs, etc.
COPY . .

# Força a remoção de um build antigo, se houver, para evitar conflitos
RUN rm -rf .next

# Executa o build de produção
RUN npm run build

# ==================================================================
# PASSO DE DEPURAÇÃO: Liste o conteúdo da pasta .next
# Isso nos mostrará se a pasta 'standalone' foi criada.
# ==================================================================
RUN ls -la .next

# Estágio 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Cria um usuário com menos privilégios
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copia os artefatos de build do estágio anterior
# Esta é a parte que estava falhando
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
