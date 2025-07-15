from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas # Seus módulos de CRUD, Models e Schemas
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cria as tabelas no banco de dados (apenas se não existirem)
models.Base.metadata.create_all(bind=engine)

# Configuração de CORS mais segura
origins = [
    "http://localhost",
    "http://localhost:3000", # Endereço do frontend em desenvolvimento
    # "https://seu-dominio-de-producao.com", # Adicionar o domínio de produção aqui
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
    return {"message": "Bem-vindo à API do Setor Musical MS"}

# Exemplo de rota utilizando a injeção de dependência do banco de dados
@app.get("/instrumentos/", response_model=list[schemas.Instrumento])
def read_instrumentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    instrumentos = crud.get_instrumentos(db, skip=skip, limit=limit)
    return instrumentos

