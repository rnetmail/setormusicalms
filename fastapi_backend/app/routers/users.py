# fastapi_backend/app/routers/users.py
# Versão 15 16/07/2025 21:58
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import get_db
from auth.security import get_current_superuser

# Define um router específico para os endpoints de usuários.
# O prefixo '/users' será adicionado a todas as rotas definidas aqui.
router = APIRouter(prefix="/users")

@router.post("/", response_model=schemas.User, status_code=201)
def create_user_endpoint(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    # Apenas superusuários podem criar novos usuários.
    current_user: models.User = Depends(get_current_superuser)
):
    """Endpoint para criar um novo usuário."""
    if crud.user.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Usuário com este username já existe.")
    if crud.user.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Usuário com este e-mail já existe.")
    
    return crud.user.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # Apenas superusuários podem listar todos os usuários.
    current_user: models.User = Depends(get_current_superuser)
):
    """Endpoint para listar todos os usuários."""
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    # Apenas superusuários podem ver os detalhes de outros usuários.
    current_user: models.User = Depends(get_current_superuser)
):
    """Endpoint para obter os detalhes de um usuário específico pelo ID."""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user_endpoint(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    # Apenas superusuários podem atualizar usuários.
    current_user: models.User = Depends(get_current_superuser)
):
    """Endpoint para atualizar os dados de um usuário."""
    db_user = crud.user.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.delete("/{user_id}", status_code=204)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    # Apenas superusuários podem apagar usuários.
    current_user: models.User = Depends(get_current_superuser)
):
    """Endpoint para apagar um usuário."""
    db_user = crud.user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    # Retorna uma resposta vazia com status 204 No Content, como é comum para DELETE.
    return
