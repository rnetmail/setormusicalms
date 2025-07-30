# fastapi_backend/app/main.py
# Versão 06 - 29/07/2025 05:05 - Estrutura a aplicação a partir deste ponto de entrada

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# CORREÇÃO: Importa os roteadores da subpasta 'routers'
from .routers import auth, users, recados, agenda, historia, galeria, repertorio

app = FastAPI(title="Setor Musical MS API")

# Configuração do CORS
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

# Roteador principal da API com o prefixo /api
api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(recados.router, prefix="/recados", tags=["Recados"])
api_router.include_router(agenda.router, prefix="/agenda", tags=["Agenda"])
api_router.include_router(historia.router, prefix="/historia", tags=["Historia"])
api_router.include_router(galeria.router, prefix="/galeria", tags=["Galeria"])
api_router.include_router(repertorio.router, prefix="/repertorio", tags=["Repertorio"])

app.include_router(api_router, prefix="/api")

@app.get("/health", tags=["Health Check"])
def health_check():
    """Verifica a saúde da aplicação, agora sem o prefixo /api."""
    return {"status": "healthy"}

