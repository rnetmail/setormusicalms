# setormusicalms/backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tenta obter a URL do banco de dados da variável de ambiente.
# Se não estiver definida, usa o valor padrão para produção dentro do Docker.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////app/data/setormusical.db")

# Garante que o diretório de dados exista antes de tentar criar o arquivo do DB,
# mas apenas se não estivermos usando um banco de dados em memória.
if "sqlite:///" in DATABASE_URL and ":memory:" not in DATABASE_URL:
    db_path = DATABASE_URL.split(":///")[1]
    db_dir = os.path.dirname(db_path)
    if db_dir: # Só cria o diretório se ele for especificado
        os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para ser usada nas rotas da API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
