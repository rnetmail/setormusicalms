# fastapi_backend/app/database.py
# Versão 03 17/07/2025 23:40
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Lógica para determinar os argumentos de conexão com base no tipo de banco de dados
connect_args = {}
database_url = settings.DATABASE_URL

# Se for SQLite, adiciona o argumento 'check_same_thread'.
# Isto é necessário porque o SQLite por padrão só permite acesso da mesma thread.
# O FastAPI, por ser assíncrono, pode usar múltiplas threads para uma única requisição.
if database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    
    # Garante que o diretório para o ficheiro do banco de dados exista.
    # Ex: sqlite:///./data/setormusical.db -> garante que a pasta /data exista.
    db_path = database_url.split(":///")[1]
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

# Cria a engine do SQLAlchemy com a URL do banco de dados e os argumentos corretos
engine = create_engine(
    database_url,
    connect_args=connect_args
)

# Cria uma classe SessionLocal que será usada para criar sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que será herdada por todos os nossos modelos ORM (tabelas)
Base = declarative_base()

def get_db():
    """
    Função de dependência do FastAPI para obter uma sessão do banco de dados por requisição.
    Utiliza um bloco try/finally para garantir que a sessão seja sempre fechada após o uso,
    liberando a conexão de volta para o pool.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
