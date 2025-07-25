# fastapi_backend/app/main.py
# Versão 02 25/07/2025 17:35
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# CORREÇÃO: As importações foram alteradas de relativas ("..") para absolutas.
from .database import engine, Base
from .config   import settings
from .routers  import auth, users, repertorio, agenda, recados, historia, galeria

# Cria todas as tabelas no banco de dados se não existirem.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.0"
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
api_router.include_router(galeria.router)

@api_router.get("/health", tags=["Health Check"])
def health_check():
    """Endpoint de verificação de saúde para monitoramento."""
    return {"status": "healthy", "message": "API está no ar e funcionando."}

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para uma verificação básica de que o serviço está online."""
    return {"message": "Bem-vindo à API do Setor Musical MS"}
