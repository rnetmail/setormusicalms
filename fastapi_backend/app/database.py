# fastapi_backend/app/database.py
# Versão 09 16/07/2025 21:18
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Lógica para determinar os argumentos de conexão com base no tipo de banco de dados
connect_args = {}
database_url = settings.DATABASE_URL

# CORREÇÃO: Se for SQLite, adiciona o argumento 'check_same_thread'.
# Isto é necessário porque o SQLite por padrão só permite acesso da mesma thread.
# O FastAPI, por ser assíncrono, pode usar múltiplas threads.
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    
    # Garante que o diretório para o ficheiro do banco de dados exista.
    # Ex: /app/data/setormusical.db -> garante que /app/data exista.
    db_path = database_url.split(":///")[1]
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

# Cria a engine do SQLAlchemy com os argumentos corretos
engine = create_engine(
    database_url,
    connect_args=connect_args
)

# Cria uma classe SessionLocal que será usada para criar sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que será usada pelos nossos modelos (tabelas) do ORM
Base = declarative_base()

def get_db():
    """
    Função de dependência do FastAPI para obter uma sessão do banco de dados por requisição.
    Garante que a sessão seja sempre fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
