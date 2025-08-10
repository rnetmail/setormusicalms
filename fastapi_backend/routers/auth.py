# /fastapi_backend/routers/auth.py
# v4.0 - 2025-08-10 20:35 - Fix ImportError - Remove app folder references

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

# Importações corrigidas - sem referência à pasta app
from schemas import token as token_schemas
from schemas import user as user_schemas
from database import get_db
from crud import user as crud_user
from auth.security import create_access_token, verify_password
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=token_schemas.Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
        """
            Endpoint de login que retorna um token de acesso.
                """
        # Busca o usuário no banco de dados
        user = crud_user.get_user_by_username(db, username=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
                raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Credenciais incorretas",
                                headers={"WWW-Authenticate": "Bearer"},
                )

    # Cria o token de acesso
    access_token = create_access_token(data={"sub": user.username})

    return {
                "access_token": access_token,
                "token_type": "bearer"
    }

@router.get("/me", response_model=user_schemas.User)
def read_users_me(current_user: user_schemas.User = Depends(crud_user.get_current_active_user)):
        """
            Retorna os dados do usuário autenticado.
                """
        return current_user
