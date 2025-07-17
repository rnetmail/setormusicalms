# fastapi_backend/app/routers/auth.py
# Versão 17 16/07/2025 22:05
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from auth.security import create_access_token, get_current_active_user

# Define o router com o prefixo '/auth' para todos os endpoints neste ficheiro.
router = APIRouter(prefix="/auth")

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
    # A dependência OAuth2PasswordRequestForm extrai o username e a password
    # do corpo da requisição, que vem no formato 'x-www-form-urlencoded'.
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint para autenticar um usuário e retornar um token de acesso.
    """
    # Usa a função do CRUD para verificar se o usuário e a senha são válidos.
    user = crud.user.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        # Se a autenticação falhar, lança uma exceção HTTP 401.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Se a autenticação for bem-sucedida, cria o token de acesso.
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
def read_users_me(
    # Esta dependência protege o endpoint. Se o token não for válido ou não for enviado,
    # a requisição será bloqueada com um erro 401 antes mesmo de o código da função executar.
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Endpoint protegido para obter os dados do usuário atualmente autenticado.
    """
    return current_user
