# setormusicalms\routers\auth.py
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # ATENÇÃO: Lógica de autenticação FAKE para desenvolvimento.
    # A lógica de validação real seria assim:
    # 1. Buscar o usuário no banco de dados pelo form_data.username
    # 2. Se o usuário existir, verificar a senha com: pwd_context.verify(form_data.password, user.hashed_password)
    
    # Por enquanto, mantemos a lógica simples para validação do endpoint.
    is_password_correct = pwd_context.verify("admin", pwd_context.hash("admin")) # Simula uma verificação
    if form_data.username == "admin" and is_password_correct:
        # Simula a criação de um token de acesso
        access_token = f"fake-token-for-user-{form_data.username}"
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos")