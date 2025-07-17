# fastapi_backend/app/database.py
# Versão 02 17/07/2025 16:38
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Lógica para determinar os argumentos de conexão com base no tipo de banco de dados
connect_args = {}
# A URL do banco de dados é lida diretamente do objeto de configurações.
database_url = settings.DATABASE_URL

# Se for SQLite, é necessário adicionar o argumento 'check_same_thread'.
# Isto é essencial porque o SQLite, por padrão, só permite acesso da mesma thread,
# [cite_start]e o FastAPI, por ser assíncrono, pode usar múltiplas threads. [cite: 2]
if database_url and database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    
    # Garante que o diretório para o ficheiro do banco de dados exista.
    # Ex: a partir de 'sqlite:///data/setormusical.db', garante que o diretório '/app/data' exista dentro do container.
    db_path = database_url.split(":///")[1]
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

# Cria a engine do SQLAlchemy com a URL e os argumentos de conexão corretos.
engine = create_engine(
    database_url,
    connect_args=connect_args
)

# Cria uma classe SessionLocal que será usada para criar sessões do banco de dados a cada requisição.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que será herdada por todos os nossos modelos do ORM (ex: User, RepertorioItem).
Base = declarative_base()

def get_db():
    """
    Função de dependência (dependency) do FastAPI para obter uma sessão do banco de dados.
    Esta função garante que a sessão do banco de dados seja aberta no início da
    [cite_start]requisição e devidamente fechada ao final, mesmo que ocorram erros. [cite: 124, 127]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
