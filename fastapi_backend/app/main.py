# fastapi_backend/app/main.py
# Versão 20 21/07/2025 18:15
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Importações absolutas da estrutura do projeto
from app.database import engine, Base
from app.config import settings
from app.routers import auth, users, repertorio, agenda, recados, historia, galeria

# Cria todas as tabelas no banco de dados se não existirem.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="2.0.0"
)

# Configura o CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria um router principal para organizar todos os endpoints sob o prefixo /api
api_router = APIRouter(prefix="/api")

# Inclui os routers de cada módulo na API principal
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(repertorio.router)
api_router.include_router(agenda.router)
api_router.include_router(recados.router)
api_router.include_router(historia.router)
api_router.include_router(galeria.router) # <-- NOVA LINHA ADICIONADA

@api_router.get("/health", tags=["Health Check"])
def health_check():
    """Endpoint de verificação de saúde para monitoramento e health checks do CI/CD."""
    return {"status": "healthy", "message": "API está no ar e funcionando."}

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para uma verificação básica de que o serviço está online."""
    return {"message": "Bem-vindo à API do Setor Musical MS"}
