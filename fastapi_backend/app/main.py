# fastapi_backend/app/main.py
# Versão 03 17/07/2025 16:39
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Importações unificadas e centralizadas
from .database import engine, Base
from .config import settings
from .routers import auth, users, repertorio, agenda, recados

# Para ambientes de desenvolvimento e teste, create_all é útil para criar o DB rapidamente.
# Em produção, um sistema de migrações como Alembic (já nos requirements) é o ideal.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.0"
)

# Configura o CORS (Cross-Origin Resource Sharing) a partir das configurações centralizadas.
# Isto é crucial para a segurança e para permitir que o frontend se comunique com a API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria um router principal para organizar todos os endpoints sob o prefixo /api.
# Esta é uma boa prática para versionamento e organização da API.
api_router = APIRouter(prefix="/api")

# Inclui os routers de cada módulo da aplicação.
api_router.include_router(auth.router, tags=["Autenticação"])
api_router.include_router(users.router, tags=["Usuários"])
api_router.include_router(repertorio.router, tags=["Repertório"])
api_router.include_router(agenda.router, tags=["Agenda"])
api_router.include_router(recados.router, tags=["Recados"])

@api_router.get("/health", tags=["Health Check"])
def health_check():
    """Endpoint de verificação de saúde para monitoramento e health checks."""
    return {"status": "healthy", "message": "API está no ar e funcionando."}

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz da API. Útil para uma verificação rápida de que o serviço está online.
    """
    return {"message": "Bem-vindo à API do Setor Musical MS"}
