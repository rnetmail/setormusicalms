# fastapi_backend/app/routers/auth.py
# Versão 01 25/07/2025 14:05
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..app.database import get_db
from ..auth.security import create_access_token, get_current_active_user
from ..crud import user as crud_user
from ..models import user as model_user
from ..schemas import user as schema_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/login", response_model=schema_user.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica um usuário com username e password e retorna um token de acesso JWT.
    """
    user = crud_user.authenticate_user(
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


@router.get("/me", response_model=schema_user.User)
def read_users_me(
    current_user: model_user.User = Depends(get_current_active_user)
):
    """
    Endpoint protegido que retorna os dados do usuário autenticado.
    """
    return current_user
