# 📚 Documentação Técnica - Setor Musical MS

## 🏗️ Arquitetura do Sistema

### Visão Geral
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (React)       │◄──►│   (Django)      │◄──►│ (PostgreSQL)    │
│   Port: 8001    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │     Docker      │    │    Volumes      │
│   (Proxy)       │    │  (Container)    │    │  (Persistent)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes

#### Frontend (React + TypeScript)
- **Framework**: React 18 com TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **State**: Context API + useState/useEffect
- **HTTP Client**: Fetch API nativo

#### Backend (Django + DRF)
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Authentication**: Token-based
- **Database ORM**: Django ORM
- **CORS**: django-cors-headers
- **Server**: Gunicorn (produção)

#### Database (PostgreSQL)
- **Version**: PostgreSQL 14 Alpine
- **Persistence**: Docker volumes
- **Backup**: pg_dump automático
- **Health Check**: pg_isready

## 🗂️ Estrutura de Dados

### Modelos Django

#### RepertorioItem
```python
class RepertorioItem(models.Model):
    type = models.CharField(max_length=20)  # 'Coral' ou 'Orquestra'
    title = models.CharField(max_length=200)
    arrangement = models.CharField(max_length=200)
    year = models.IntegerField()
    audioUrl = models.URLField(blank=True)
    videoUrl = models.URLField(blank=True)
    sheetMusicUrl = models.URLField(blank=True)
    naipes = models.JSONField(default=list)  # Para coral
    grupos = models.JSONField(default=list)  # Para orquestra
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### AgendaItem
```python
class AgendaItem(models.Model):
    group = models.CharField(max_length=20)  # 'Coral', 'Orquestra', 'Setor'
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### RecadoItem
```python
class RecadoItem(models.Model):
    group = models.CharField(max_length=20)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### HistoriaItem
```python
class HistoriaItem(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    imageUrl = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### GaleriaItem
```python
class GaleriaItem(models.Model):
    group = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    imageUrl = models.URLField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Relacionamentos
- Todos os modelos são independentes (sem FK)
- Filtros por `group` para separar Coral/Orquestra
- Campo `active` para soft delete
- Timestamps automáticos

## 🔌 APIs REST

### Endpoints Principais

#### Autenticação
```
POST /api/auth/login/
Body: {"username": "admin", "password": "senha"}
Response: {"token": "abc123...", "user": {...}}

POST /api/auth/logout/
Headers: Authorization: Token abc123...
Response: {"message": "Logout successful"}
```

#### Repertório
```
GET /api/repertorio/
Query: ?type=Coral&active=true
Response: [{"id": 1, "title": "Ave Maria", ...}]

POST /api/repertorio/
Headers: Authorization: Token abc123...
Body: {"type": "Coral", "title": "Nova música", ...}

PUT /api/repertorio/{id}/
PATCH /api/repertorio/{id}/
DELETE /api/repertorio/{id}/
```

#### Agenda
```
GET /api/agenda/
Query: ?group=Coral&date_gte=2024-01-01
Response: [{"id": 1, "title": "Ensaio", "date": "2024-01-15", ...}]

POST /api/agenda/
PUT /api/agenda/{id}/
DELETE /api/agenda/{id}/
```

#### Recados
```
GET /api/recados/
POST /api/recados/
PUT /api/recados/{id}/
DELETE /api/recados/{id}/
```

#### História
```
GET /api/historia/
POST /api/historia/
PUT /api/historia/{id}/
DELETE /api/historia/{id}/
```

#### Galeria
```
GET /api/galeria/
POST /api/galeria/
PUT /api/galeria/{id}/
DELETE /api/galeria/{id}/
```

### Autenticação e Permissões

#### Token Authentication
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
```

#### Permissões por Endpoint
- **GET (Leitura)**: Público (sem autenticação)
- **POST/PUT/PATCH/DELETE**: Autenticado (token required)
- **Admin**: Acesso total via Django Admin

## 🎨 Frontend Architecture

### Estrutura de Componentes
```
src/
├── components/
│   ├── common/          # Componentes reutilizáveis
│   ├── layout/          # Layout e navegação
│   └── forms/           # Formulários
├── pages/               # Páginas principais
├── contexts/            # Context API
├── hooks/               # Custom hooks
├── services/            # API calls
├── types/               # TypeScript types
└── utils/               # Utilitários
```

### Roteamento
```typescript
// App.tsx
<Routes>
  <Route path="/" element={<HomePage />} />
  <Route path="/coral/*" element={<CoralRoutes />} />
  <Route path="/orquestra/*" element={<OrquestraRoutes />} />
  <Route path="/gestao/*" element={<AdminRoutes />} />
</Routes>
```

### Estado Global
```typescript
// AuthContext.tsx
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}
```

### Serviços API
```typescript
// services/api.ts
class ApiService {
  private baseURL = '/api';
  private token = localStorage.getItem('token');

  async get<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      headers: this.getHeaders(),
    });
    return response.json();
  }

  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    });
    return response.json();
  }

  private getHeaders() {
    return {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Token ${this.token}` }),
    };
  }
}
```

## 🐳 Docker Configuration

### docker-compose.yml
```yaml
services:
  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: ./backend
    environment:
      SECRET_KEY: ${SECRET_KEY}
      DEBUG: ${DEBUG}
      POSTGRES_DB: ${POSTGRES_DB}
      # ... outras variáveis
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: .
    ports:
      - "8001:80"
    depends_on:
      backend:
        condition: service_healthy
```

### Dockerfile (Frontend)
```dockerfile
# Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Dockerfile (Backend)
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN mkdir -p /app/static /app/media

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

#### Deploy Workflow (.github/workflows/deploy.yml)
```yaml
name: Deploy to VPS
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.message, 'Deploy to VPS')
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        
    - name: Build frontend
      run: |
        npm ci
        npm run build
        
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Test backend
      run: |
        cd backend
        pip install -r requirements.txt
        python manage.py check
        
    - name: Deploy to VPS
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.VPS_HOST }}
        username: ${{ secrets.USER_ADMIN }}
        password: ${{ secrets.VPS_SSH_PASS }}
        script: |
          cd /setormusical/setormusicalms
          git pull origin main
          docker-compose down
          docker-compose build --no-cache
          docker-compose up -d
```

#### CI Workflow (.github/workflows/ci.yml)
```yaml
name: Continuous Integration
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npm run build
    - run: npm run lint
    
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
    - run: |
        cd backend
        pip install -r requirements.txt
        python manage.py test
```

## 🔒 Segurança

### Configurações Django
```python
# settings.py (produção)
DEBUG = False
ALLOWED_HOSTS = ['setormusicalms.art.br']
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
```

### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "https://setormusicalms.art.br",
]
CORS_ALLOW_CREDENTIALS = True
```

### Token Security
- Tokens armazenados em localStorage (frontend)
- Expiração automática configurável
- Logout limpa tokens
- Headers Authorization obrigatórios

## 📊 Monitoramento e Logs

### Health Checks
```bash
# Verificar saúde dos serviços
curl -f http://localhost:8001/health
curl -f http://localhost:8001/api/health
docker-compose exec db pg_isready
```

### Logging Configuration
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

### Métricas
- Response time por endpoint
- Error rate por serviço
- Database connection pool
- Memory/CPU usage

## 🔧 Configuração de Ambiente

### Variáveis de Ambiente
```bash
# .env (produção)
SECRET_KEY=sua-chave-super-secreta-aqui
DEBUG=0
ALLOWED_HOSTS=setormusicalms.art.br
POSTGRES_DB=setormusicalms_db
POSTGRES_USER=mestre
POSTGRES_PASSWORD=Setor@MS25
SQL_HOST=db
SQL_PORT=5432
CORS_ALLOWED_ORIGINS=https://setormusicalms.art.br
ADMIN_USER=admin
ADMIN_PASS=Setor@MS25
```

### Secrets GitHub
```
VPS_HOST=setormusicalms@ip-194-195-221-198.cloudezapp.io
VPS_SSH_PASS=Setor@MS25
VPS_SSH_PORT=22
USER_ADMIN=setormusicalms
```

## 🚀 Performance

### Frontend Optimizations
- Code splitting com React.lazy
- Bundle optimization com Vite
- Image lazy loading
- CSS minification

### Backend Optimizations
- Database indexing
- Query optimization
- Static files serving
- Gunicorn workers

### Caching Strategy
- Browser caching (static assets)
- API response caching (futuro)
- Database query caching (futuro)

---

**📖 Documentação mantida atualizada com cada deploy**

