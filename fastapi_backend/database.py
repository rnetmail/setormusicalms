# /fastapi_backend/database.py
# v3.0 - 2025-08-12 - Configurado para usar exclusivamente PostgreSQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Importação direta do config
from config import settings

# Cria a engine do SQLAlchemy com a URL do banco de dados PostgreSQL
engine = create_engine(
    settings.DATABASE_URL
)

# Cria uma classe SessionLocal que será usada para criar sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que será herdada por todos os nossos modelos ORM (tabelas)
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