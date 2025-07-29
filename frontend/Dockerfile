# frontend/Dockerfile - Otimizado para Next.js

# Estágio 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Instala dependências primeiro para aproveitar o cache do Docker
COPY package.json package-lock.json ./
RUN npm install

# Copia o resto do código do frontend
COPY . .

# Executa o build de produção do Next.js
RUN npm run build

# Estágio 2: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Cria um usuário com menos privilégios para segurança
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

# Copia os artefatos de build otimizados do estágio anterior
# A pasta 'standalone' é criada pelo 'output: standalone' no next.config.js
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

EXPOSE 3000

# Inicia o servidor Node.js otimizado do Next.js
CMD ["node", "server.js"]
