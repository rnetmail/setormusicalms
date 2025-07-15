// D:\setormusicalms\routers\auth.py
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # ATENÇÃO: Lógica de autenticação FAKE para desenvolvimento.
    # TODO: Substituir pela validação real do usuário e senha no banco de dados.
    if form_data.username == "admin" and form_data.password == "admin":
        # Simula a criação de um token de acesso
        access_token = f"fake-token-for-user-{form_data.username}"
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos")