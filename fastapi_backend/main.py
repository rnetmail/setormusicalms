# /fastapi_backend/app/main.py
# v3.0 - 2025-08-06 17:32:00 - Simplifica importações e corrige estrutura.

from fastapi import FastAPI
from routers import auth, users, recados, agenda, historia, galeria, repertorio
from fastapi.middleware.cors import CORSMiddleware

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
    "*"  # Para desenvolvimento
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical MS", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend"}

@app.get("/api/health")
def api_health_check():
    return {"status": "ok", "service": "api"}

# Importações condicionais para evitar erros de inicialização
try:
    from .database import engine, Base
    # Cria as tabelas no banco de dados (se não existirem)
    Base.metadata.create_all(bind=engine)
    
    # Importa e inclui as rotas apenas se as dependências estiverem disponíveis
    from .routers import auth, users, recados, agenda, historia, galeria, repertorio
    
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/users", tags=["users"])
    app.include_router(recados.router, prefix="/api/recados", tags=["recados"])
    app.include_router(agenda.router, prefix="/api/agenda", tags=["agenda"])
    app.include_router(historia.router, prefix="/api/historia", tags=["historia"])
    app.include_router(galeria.router, prefix="/api/galeria", tags=["galeria"])
    app.include_router(repertorio.router, prefix="/api/repertorio", tags=["repertorio"])
    
except ImportError as e:
    print(f"Aviso: Algumas rotas não puderam ser carregadas: {e}")
    print("A API básica ainda funcionará, mas algumas funcionalidades podem não estar disponíveis.")

except Exception as e:
    print(f"Erro durante a inicialização: {e}")
    print("A API básica ainda funcionará.")
