# /fastapi_backend/main.py
# v5.0 - 2025-08-08 - Final, com estrutura simplificada e importações diretas.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- CORREÇÃO ---
# Importa os módulos e o objeto Base diretamente.
import database
from routers import auth, users, recados, agenda, historia, galeria, repertorio

# Cria as tabelas no banco de dados ao iniciar a aplicação.
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para o sistema de gerenciamento do Setor Musical.",
    version="1.0.0"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8001",
    "https://setormusicalms.art.br",
    "http://setormusicalms.art.br",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )

# Inclui as rotas na aplicação
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(recados.router)
app.include_router(agenda.router)
app.include_router(historia.router)
app.include_router(galeria.router)
app.include_router(repertorio.router)

# Endpoints básicos de saúde
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical MS", "status": "ok"}

@app.get("/api/health")
def api_health_check():
    return {"status": "ok", "service": "api"}
