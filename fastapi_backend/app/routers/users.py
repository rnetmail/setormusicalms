# fastapi_backend/app/routers/users.py
# Versão 03 - FINAL

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from schemas import user as schema_user
from crud import user as crud_user
from auth.security import get_current_staff_user, get_current_superuser
from models import user as model_user

router = APIRouter(prefix="/users", tags=["Usuários"])

@router.get("/", response_model=List[schema_user.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Lista todos os usuários. Apenas para administradores."""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schema_user.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schema_user.UserCreate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_superuser)
):
    """Cria um novo usuário. Apenas para superusuários."""
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já registrado")
    return crud_user.create_user(db=db, user=user)

# ... (O restante do arquivo permanece o mesmo)
