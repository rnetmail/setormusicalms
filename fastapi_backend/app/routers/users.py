# /fastapi_backend/app/routers/users.py
# v2.0 - 2025-07-30 22:58:00 - Corrige importações para estrutura correta do projeto.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações corretas baseadas na estrutura real do projeto
from ...schemas import user as user_schemas
from ..database import get_db
from ...crud import user as crud_user

router = APIRouter()

@router.post("/", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no banco de dados.
    """
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[user_schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de usuários.
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=user_schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna um usuário específico pelo ID.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

