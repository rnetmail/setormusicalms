# 🚀 Guia de Deploy - Setor Musical MS

Este guia detalha o processo de deploy automático e manual do sistema.

## 📋 Pré-requisitos

### No GitHub
- Repositório configurado com secrets:
  - `VPS_HOST`: Host da VPS
  - `VPS_SSH_PASS`: Senha SSH
  - `VPS_SSH_PORT`: Porta SSH (22)
  - `USER_ADMIN`: Usuário admin

### Na VPS
- Docker e Docker Compose instalados
- Nginx externo configurado (porta 8001 → aplicação)
- Diretório `/setormusical/setormusicalms` criado
- Permissões adequadas para o usuário

## 🔄 Deploy Automático (Recomendado)

### 1. Processo Simples
```bash
# 1. Faça suas alterações
git add .
git commit -m "Deploy to VPS - Suas alterações aqui"
git push origin main
```

### 2. Workflow Executado
O GitHub Actions executará automaticamente:

1. **Build Frontend** (≈ 2 min)
   - Instala dependências Node.js
   - Executa build do React/Vite
   - Valida build sem erros

2. **Validação Backend** (≈ 1 min)
   - Instala dependências Python
   - Executa Django checks
   - Valida configurações

3. **Deploy na VPS** (≈ 3-5 min)
   - Conecta via SSH
   - Sincroniza código
   - Build das imagens Docker
   - Restart dos containers
   - Health checks

4. **Validação Final** (≈ 1 min)
   - Testa frontend (porta 8001)
   - Testa backend (Django checks)
   - Testa banco (PostgreSQL)
   - Logs de status

### 3. Monitoramento
- Acompanhe em: `https://github.com/rnetmail/setormusicalms/actions`
- Logs detalhados disponíveis
- Notificações de sucesso/falha

## 🛠️ Deploy Manual (Emergência)

### 1. Acesso SSH
```bash
ssh setormusicalms@ip-194-195-221-198.cloudezapp.io -p 22
cd /setormusical/setormusicalms
```

### 2. Atualização do Código
```bash
# Backup atual
docker-compose down
git stash  # Se houver alterações locais

# Atualizar código
git fetch origin
git reset --hard origin/main
```

### 3. Rebuild e Restart
```bash
# Build das imagens
docker-compose build --no-cache

# Iniciar serviços
docker-compose up -d

# Verificar status
docker-compose ps
docker-compose logs --tail=50
```

### 4. Validação Manual
```bash
# Testar containers
docker-compose exec backend python manage.py check
docker-compose exec db pg_isready -U mestre

# Testar endpoints
curl -f http://localhost:8001
curl -f http://localhost:8001/api/
```

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Build Frontend Falha
```bash
# Limpar cache npm
npm ci --cache /tmp/empty-cache

# Verificar dependências
npm audit fix
```

#### 2. Backend Não Inicia
```bash
# Verificar logs
docker-compose logs backend

# Verificar banco
docker-compose logs db

# Restart específico
docker-compose restart backend
```

#### 3. Banco de Dados
```bash
# Verificar conexão
docker-compose exec db pg_isready -U mestre

# Executar migrações
docker-compose exec backend python manage.py migrate

# Verificar dados
docker-compose exec backend python manage.py shell
```

#### 4. Problemas de Rede
```bash
# Verificar portas
netstat -tlnp | grep 8001

# Verificar containers
docker network ls
docker network inspect setormusicalms_network
```

### Logs Importantes

#### Workflow GitHub Actions
```bash
# Verificar em:
https://github.com/rnetmail/setormusicalms/actions

# Logs específicos:
- Build Frontend
- Backend Tests  
- Deploy to VPS
- Health Checks
```

#### Logs da Aplicação
```bash
# Todos os serviços
docker-compose logs --tail=100

# Serviço específico
docker-compose logs frontend --tail=50
docker-compose logs backend --tail=50
docker-compose logs db --tail=20

# Logs em tempo real
docker-compose logs -f backend
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

#### Produção (.env)
```bash
SECRET_KEY=sua-chave-secreta-super-forte
DEBUG=0
ALLOWED_HOSTS=setormusicalms.art.br
POSTGRES_DB=setormusicalms_db
POSTGRES_USER=mestre
POSTGRES_PASSWORD=Setor@MS25
CORS_ALLOWED_ORIGINS=https://setormusicalms.art.br
```

#### Desenvolvimento (.env.local)
```bash
SECRET_KEY=dev-key-not-secure
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=setormusicalms_dev
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_pass
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Health Checks

#### Configuração Docker
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 60s
```

#### Verificação Manual
```bash
# Frontend
curl -f http://localhost:8001

# Backend
curl -f http://localhost:8001/api/

# Banco
docker-compose exec db pg_isready -U mestre
```

## 📊 Monitoramento Contínuo

### Métricas Importantes
- **Uptime**: Disponibilidade dos serviços
- **Response Time**: Tempo de resposta
- **Error Rate**: Taxa de erros
- **Resource Usage**: CPU, Memória, Disco

### Alertas Configurados
- Container down
- High error rate
- Database connection issues
- Disk space low

### Backup Strategy
```bash
# Backup automático (cron)
0 2 * * * docker-compose exec db pg_dump -U mestre setormusicalms_db > /backup/db_$(date +%Y%m%d).sql

# Backup manual
docker-compose exec db pg_dump -U mestre setormusicalms_db > backup.sql

# Restore
docker-compose exec -T db psql -U mestre setormusicalms_db < backup.sql
```

## 🚨 Procedimentos de Emergência

### 1. Site Fora do Ar
```bash
# Verificação rápida
curl -I https://setormusicalms.art.br

# Restart completo
docker-compose down
docker-compose up -d

# Verificar logs
docker-compose logs --tail=100
```

### 2. Rollback Rápido
```bash
# Voltar para commit anterior
git log --oneline -5
git reset --hard COMMIT_ANTERIOR
docker-compose down
docker-compose up -d --build
```

### 3. Backup de Emergência
```bash
# Backup completo
docker-compose exec db pg_dump -U mestre setormusicalms_db > emergency_backup.sql
tar -czf emergency_backup.tar.gz emergency_backup.sql docker-compose.yml .env
```

## 📞 Contatos de Suporte

- **Repositório**: https://github.com/rnetmail/setormusicalms
- **Issues**: https://github.com/rnetmail/setormusicalms/issues
- **Actions**: https://github.com/rnetmail/setormusicalms/actions

---

**⚡ Deploy automatizado para máxima eficiência!**

