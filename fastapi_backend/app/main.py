# fastapi_backend/app/main.py
# Versão 84 18/07/2025 09:55
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, users, repertorio, agenda, recados
import models

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

# Rotas principais da API
api_router.include_router(auth.router, tags=["Autenticação"])
api_router.include_router(users.router, tags=["Usuários"])
api_router.include_router(repertorio.router, tags=["Repertório"])
api_router.include_router(agenda.router, tags=["Agenda"])
api_router.include_router(recados.router, tags=["Recados"])

# CORREÇÃO: A rota de health check agora está dentro do 'api_router'.
@api_router.get("/health", tags=["Health Check"])
def health_check():
    """Endpoint de verificação de saúde para monitoramento."""
    return {"status": "healthy"}

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para uma verificação básica de que a API está no ar."""
    return {"status": "ok"}
