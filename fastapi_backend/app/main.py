# /fastapi_backend/app/main.py
# v2.0 - 2025-07-30 22:55:00 - Corrige importações para estrutura correta do projeto.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importações corretas baseadas na estrutura real do projeto
from .database import engine, Base
from .routers import auth, users, recados, agenda, historia, galeria, repertorio

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para o sistema de gerenciamento do Setor Musical.",
    version="1.0.0"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    # Adicione aqui o endereço do seu frontend em produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os roteadores com o prefixo /api
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(recados.router, prefix="/api/recados", tags=["recados"])
app.include_router(agenda.router, prefix="/api/agenda", tags=["agenda"])
app.include_router(historia.router, prefix="/api/historia", tags=["historia"])
app.include_router(galeria.router, prefix="/api/galeria", tags=["galeria"])
app.include_router(repertorio.router, prefix="/api/repertorio", tags=["repertorio"])

@app.get("/api/health", tags=["Health Check"])
def health_check():
    """Verifica a saúde da API."""
    return {"status": "ok"}

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical MS"}

