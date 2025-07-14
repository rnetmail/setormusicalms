# Setor Musical MS - Sistema de Gerenciamento

## 🎵 Sobre o Projeto

Sistema completo para gerenciamento do Setor Musical Mokiti Okada MS, incluindo:
- 🎼 **Repertório** separado por Coral e Orquestra
- 📅 **Agenda** de ensaios e apresentações
- 📢 **Recados** organizados por grupo
- 🎵 **Reprodução de mídia** com conversão automática de links

## 🚀 Tecnologias

### Backend - FastAPI
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados principal
- **SQLAlchemy** - ORM para Python
- **JWT** - Autenticação segura
- **Conversão automática** de links Google Drive e YouTube

### Frontend - React + TypeScript
- **React** - Interface de usuário
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Vite** - Build tool

## 🔧 Funcionalidades

### ✅ **Filtros por Grupo**
- **Coral:** Repertório, agenda e recados específicos
- **Orquestra:** Conteúdo separado e organizado
- **Setor:** Informações gerais

### ✅ **Conversão Automática de Mídia**
- **Google Drive Audio:** Conversão para reprodução direta
- **Google Drive PDF:** Conversão para visualização em iframe
- **YouTube:** Conversão para player embed

### ✅ **Sistema de Autenticação**
- **Login seguro** com JWT
- **Usuário admin:** admin / Setor@MS25
- **Permissões** para criação e edição

## 🏗️ Arquitetura

```
setormusicalms/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main_production.py    # Aplicação principal
│   │   └── main_working.py       # Versão de desenvolvimento
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile          # Container do backend
├── components/             # Componentes React
├── pages/                 # Páginas da aplicação
├── services/              # Serviços de API
├── docker-compose.yml     # Orquestração de containers
└── README.md             # Este arquivo
```

## 🚀 Deploy

### Desenvolvimento Local

```bash
# Clonar repositório
git clone https://github.com/rnetmail/setormusicalms.git
cd setormusicalms

# Iniciar com Docker
docker-compose up -d

# Ou iniciar manualmente
cd backend
pip install -r requirements.txt
uvicorn app.main_working:app --reload --port 8000

# Frontend
npm install
npm run dev
```

### Produção (VPS)

```bash
# Na VPS
git pull origin main
docker-compose down
docker-compose up -d --build

# Verificar status
docker-compose ps
curl http://localhost:8000/api/health
```

## 📋 API Endpoints

### **Autenticação**
- `POST /api/auth/login` - Login e obtenção de token

### **Repertório**
- `GET /api/repertorio/` - Listar todos os itens
- `GET /api/repertorio/by-group/{group_type}` - Filtrar por grupo
- `POST /api/repertorio/` - Criar novo item

### **Agenda**
- `GET /api/agenda/by-group/{group_type}` - Agenda por grupo
- `POST /api/agenda/` - Criar evento

### **Recados**
- `GET /api/recados/by-group/{group_type}` - Recados por grupo
- `POST /api/recados/` - Criar recado

## 🎵 Conversão de Mídia

### Google Drive
```
❌ Original: https://drive.google.com/file/d/FILE_ID/view
✅ Áudio: https://drive.google.com/uc?export=download&id=FILE_ID
✅ PDF: https://drive.google.com/file/d/FILE_ID/preview
```

### YouTube
```
❌ Original: https://youtu.be/VIDEO_ID
✅ Embed: https://www.youtube.com/embed/VIDEO_ID
```

## 🧪 Testes

```bash
# Testar API
curl http://localhost:8000/api/health

# Login
curl -X POST "http://localhost:8000/api/auth/login?username=admin&password=Setor@MS25"

# Testar filtros
curl "http://localhost:8000/api/repertorio/by-group/Coral"
curl "http://localhost:8000/api/agenda/by-group/Orquestra"
```

## 📞 Suporte

### Credenciais Padrão
- **Usuário:** admin
- **Senha:** Setor@MS25

### Logs
```bash
# Ver logs dos containers
docker-compose logs backend
docker-compose logs frontend

# Status da aplicação
curl http://localhost:8000/api/health
```

### Problemas Comuns

**Erro de CORS:** Verificar configuração no `main_production.py`
**Mídia não reproduz:** Verificar se links foram convertidos corretamente
**Login falha:** Verificar se usuário admin foi criado

## 📝 Changelog

### v1.0.3 - FastAPI Production
- ✅ **Migração completa** do Django para FastAPI
- ✅ **Filtros por grupo** funcionando perfeitamente
- ✅ **Conversão automática** de mídia implementada
- ✅ **CORS configurado** para produção
- ✅ **Testes automatizados** validados

### v1.0.2 - FastAPI Development
- ✅ Implementação inicial do FastAPI
- ✅ Sistema de autenticação JWT
- ✅ CRUDs básicos funcionando

### v1.0.1 - Django (Descontinuado)
- ❌ Problemas de CORS e autenticação
- ❌ Filtros não funcionavam corretamente
- ❌ Mídia não reproduzia

---

**Desenvolvido para o Setor Musical Mokiti Okada MS**  
**Versão:** 1.0.3 - FastAPI Production  
**Status:** ✅ Funcionando perfeitamente

