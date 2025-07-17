# fastapi_backend/app/routers/auth.py
# Versão 54 18/07/2025 00:01
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# CORREÇÃO: Importações diretas dos pacotes a partir da raiz do projeto
import crud
import models
import schemas
from app.database import get_db
from auth.security import create_access_token, get_current_active_user

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=schemas.user.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Endpoint para autenticar um usuário e retornar um token de acesso."""
    user = crud.user.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.user.User)
def read_users_me(
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint protegido para obter os dados do usuário atualmente autenticado."""
    return current_user
