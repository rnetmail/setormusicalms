# /fastapi_backend/app/routers/auth.py
# v3.1 - 2025-08-07 - Mantido para consistência.

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

# Importações absolutas (exemplo, caso fossem necessárias)
# from app.schemas import token as token_schemas
# from app.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# Endpoint básico de login para teste
@router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint básico de login para teste.
    """
    # Validação básica para teste
    if form_data.username == "admin" and form_data.password == "admin":
        return {
            "access_token": "token-de-teste", 
            "token_type": "bearer",
            "message": "Login realizado com sucesso"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me")
def read_users_me():
    """
    Retorna dados básicos do usuário para teste.
    """
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@setormusical.ms",
        "is_active": True
    }
