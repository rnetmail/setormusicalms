# fastapi_backend/app/routers/auth.py
# Versão 02 26/07/2025 02:30
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# CORREÇÃO: Import absoluto a partir da raiz do projeto 'app'
from app.database import get_db
from schemas import user as schema_user, token as schema_token
from crud import user as crud_user
from auth.security import create_access_token, get_current_active_user, authenticate_user
from app.config import settings
from models import user as model_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=schema_token.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
