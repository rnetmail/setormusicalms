# /fastapi_backend/main.py
# v4.0 - 2025-08-08 - Final, com estrutura simplificada e importações absolutas.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- INÍCIO DA CORREÇÃO ---
# Importa os módulos diretamente, pois agora estão na mesma raiz.
import database
from routers import auth, users, recados, agenda, historia, galeria, repertorio
# --- FIM DA CORREÇÃO ---

# Cria as tabelas no banco de dados (se não existirem) ao iniciar a aplicação
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
    "http://localhost:8001", # Adicionado para o proxy local
    "https://setormusicalms.art.br", # Domínio de produção
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
