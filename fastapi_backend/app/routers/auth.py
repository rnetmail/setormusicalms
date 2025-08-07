# /fastapi_backend/app/routers/auth.py
# v3.0 - 2025-08-06 17:35:00 - Simplifica para resolver problemas de importação.

from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter()

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
