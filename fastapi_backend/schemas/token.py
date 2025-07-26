# fastapi_backend/schemas/token.py
# Versão 01 26/07/2025 11:00

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Schema para o token de acesso retornado no login."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema para os dados contidos dentro de um token JWT."""
    username: Optional[str] = None
