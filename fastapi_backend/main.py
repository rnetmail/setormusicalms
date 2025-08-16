# /fastapi_backend/main.py
# v6.0 - 2025-08-10 20:30 - Fix ImportError - Remove app folder references

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import traceback

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
    try:
        # Test database connection
        from sqlalchemy import text
        
        with database.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            db_status = "connected" if result.fetchone() else "disconnected"
        
        return {
            "status": "healthy",
            "service": "backend", 
            "database": db_status,
            "message": "API is running successfully"
        }
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy", 
            "service": "backend",
            "error": str(e),
            "database": "disconnected"
        })
