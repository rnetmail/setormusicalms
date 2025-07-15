# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# O caminho para o banco de dados agora é absoluto dentro do container,
# apontando para o volume que configuramos no docker-compose.yml.
DATABASE_URL = "sqlite:////app/data/setormusical.db"

# Garante que o diretório de dados exista antes de tentar criar o arquivo do DB
os.makedirs(os.path.dirname(DATABASE_URL.split("://")[1]), exist_ok=True)

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

