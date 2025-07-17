# fastapi_backend/app/routers/users.py
# Versão 53 18/07/2025 00:00
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# CORREÇÃO: Importações diretas dos pacotes a partir da raiz do projeto
import crud
import models
import schemas
from app.database import get_db
from auth.security import get_current_superuser

router = APIRouter(prefix="/users")

@router.post("/", response_model=schemas.user.User, status_code=201)
def create_user_endpoint(
    user: schemas.user.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_superuser)
):
    """Endpoint para criar um novo usuário."""
    if crud.user.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Usuário com este username já existe.")
    if crud.user.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Usuário com este e-mail já existe.")
    
    return crud.user.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.user.User])
def read_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_superuser)
):
    """Endpoint para listar todos os usuários."""
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.user.User)
def read_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_superuser)
):
    """Endpoint para obter os detalhes de um usuário específico pelo ID."""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.put("/{user_id}", response_model=schemas.user.User)
def update_user_endpoint(
    user_id: int,
    user_update: schemas.user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_superuser)
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
    current_user: models.user.User = Depends(get_current_superuser)
):
    """Endpoint para apagar um usuário."""
    db_user = crud.user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return
