# fastapi_backend/app/routers/users.py
# Versão 14 18/07/2025 00:00
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações absolutas, utilizando a nova estrutura de pacotes
from app.database import get_db
from auth.security import get_current_superuser
from crud import user as crud_user
from models import user as model_user
from schemas import user as schema_user

# Apenas superusuários podem acessar os endpoints deste router.
router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
    dependencies=[Depends(get_current_superuser)]
)

@router.post("/", response_model=schema_user.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schema_user.UserCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo usuário. Apenas superusuários podem executar esta ação."""
    if crud_user.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Usuário com este username já existe.")
    if crud_user.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Usuário com este e-mail já existe.")
    
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[schema_user.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os usuários. Apenas superusuários podem executar esta ação."""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schema_user.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtém os detalhes de um usuário específico pelo ID."""
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.put("/{user_id}", response_model=schema_user.User)
def update_user(
    user_id: int,
    user_update: schema_user.UserUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza os dados de um usuário."""
    db_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para atualização.")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Apaga um usuário."""
    db_user = crud_user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão.")
    # Retorna uma resposta vazia com status 204, como é a boa prática para DELETE.
    return
