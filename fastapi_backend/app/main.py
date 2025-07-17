# fastapi_backend/app/main.py
# Versão 10 16/07/2025 21:42
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter

# Importa a engine do banco de dados e a Base para criação das tabelas
from .database import engine, Base
# Importa os routers de cada módulo da aplicação
from .routers import auth, users, repertorio, agenda, recados

# Este comando é crucial: ele cria o ficheiro .db e todas as tabelas
# (users, repertorio_items, etc.) na primeira vez que a aplicação é executada.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.0"
)

# Adiciona o middleware de CORS para permitir que o frontend (em outro domínio/porta)
# possa fazer requisições para esta API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc).
    allow_headers=["*"],  # Permite todos os cabeçalhos nas requisições.
)

# Cria um router principal para agrupar todas as rotas da API sob um único prefixo.
# Isso organiza os endpoints e facilita a configuração do proxy.
api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, tags=["Autenticação"])
api_router.include_router(users.router, tags=["Usuários"])
api_router.include_router(repertorio.router, tags=["Repertório"])
api_router.include_router(agenda.router, tags=["Agenda"])
api_router.include_router(recados.router, tags=["Recados"])

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para uma verificação rápida de que a API está no ar."""
    return {"status": "ok", "message": "Bem-vindo à API do Setor Musical MS"}
