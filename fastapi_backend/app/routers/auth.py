# fastapi_backend/app/routers/auth.py
# Versão 07 - 29/07/2025 05:10 - Corrige importações relativas e dependências

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# CORREÇÃO: Usa importações relativas para funcionar dentro do módulo 'app'
from .. import crud, schemas
from ..auth import security
from ..database import get_db
from ..config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Processa o login do usuário e retorna um token de acesso JWT.
    A rota completa será /api/auth/login.
    """
    user = crud.user.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
