# fastapi_backend/app/main.py
# Versão 02 - 29/07/2025 04:35 - Adiciona o roteador da API com prefixo /api e habilita CORS

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, users, recados, agenda, historia, galeria, repertorio

# Cria a instância da aplicação FastAPI
app = FastAPI(title="Setor Musical MS API")

# Configuração do CORS para permitir requisições do frontend
# Isso é crucial para que o navegador não bloqueie as chamadas da API.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://setormusicalms.art.br",
    "https://setormusicalms.art.br",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )

# Roteador principal da API
# Inclui todos os outros roteadores de endpoints sob o prefixo /api
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(recados.router, prefix="/api/recados", tags=["recados"])
app.include_router(agenda.router, prefix="/api/agenda", tags=["agenda"])
app.include_router(historia.router, prefix="/api/historia", tags=["historia"])
app.include_router(galeria.router, prefix="/api/galeria", tags=["galeria"])
app.include_router(repertorio.router, prefix="/api/repertorio", tags=["repertorio"])

# Endpoint de verificação de saúde da aplicação
@app.get("/api/health", tags=["health"])
def read_root():
    """Endpoint para verificar se a API está online."""
    return {"status": "healthy"}
