# /fastapi_backend/app/routers/auth.py
# v2.0 - 2025-07-30 22:56:00 - Corrige importações para estrutura correta do projeto.

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Importações corretas baseadas na estrutura real do projeto
from ...schemas import user as user_schemas, token as token_schemas
from ...auth import security
from ..database import get_db
from ...crud import user as crud_user

router = APIRouter()

@router.post("/login", response_model=token_schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica o usuário e retorna um token de acesso.
    """
    user = crud_user.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=user_schemas.User)
def read_users_me(current_user: user_schemas.User = Depends(crud_user.get_current_active_user)):
    """
    Retorna os dados do usuário autenticado.
    """
    return current_user

