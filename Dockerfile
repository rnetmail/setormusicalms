# Dockerfile
# Versão 117 - FINAL PARA O FRONTEND (React + Node.js)
# ==================================================================
# Estágio 1: Builder - Instala dependências e compila a aplicação
# ==================================================================
FROM node:20-alpine AS builder

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de gerenciamento de pacotes
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

# Instala as dependências de produção e desenvolvimento
# O Next.js precisa das devDependencies para o build
RUN npm install

# Copia o resto do código-fonte da aplicação
COPY . .

# Executa o build de produção
# Esta é a linha que está faltando no seu processo!
RUN npm run build

# ==================================================================
# Estágio 2: Runner - Cria a imagem final, leve e otimizada
# ==================================================================
FROM node:20-alpine AS runner

WORKDIR /app

# Define o ambiente para produção
ENV NODE_ENV=production

# Copia o usuário 'nextjs' para rodar a aplicação com menos privilégios
# (Boa prática de segurança)
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Cria um usuário com menos privilégios
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Define o usuário para rodar a aplicação
USER nextjs

# Expõe a porta que a aplicação vai rodar
EXPOSE 3000

# Define o comando para iniciar o servidor de produção
# O host 0.0.0.0 é crucial para aceitar conexões externas ao contêiner
CMD ["node", "server.js"]```

**Observação Importante:** Este `Dockerfile` assume que você está usando a funcionalidade "Output Standalone" do Next.js, que é a melhor prática para Docker. Para ativá-la, modifique seu arquivo `next.config.mjs` (ou `.js`):

**Arquivo para modificar:** `next.config.mjs`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Adicione esta linha:
  output: 'standalone',
};

export default nextConfig;
