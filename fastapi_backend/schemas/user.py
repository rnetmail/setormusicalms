# fastapi_backend/schemas/user.py
# Versão 02 - FINAL E CORRIGIDA

from pydantic import BaseModel, EmailStr
from typing import Optional

# --- SCHEMAS BASE ---

class UserBase(BaseModel):
    """Schema base com os campos comuns de um usuário."""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    is_superuser: Optional[bool] = False

# --- SCHEMAS PARA CRIAÇÃO E ATUALIZAÇÃO ---

class UserCreate(UserBase):
    """Schema para a criação de um novo usuário."""
    password: str
    # CORREÇÃO: Garante que o full_name seja aceito durante a criação.
    full_name: str 

class UserUpdate(BaseModel):
    """Schema para atualização de um usuário. Todos os campos são opcionais."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None

# --- SCHEMA PARA RETORNO DA API ---

class User(UserBase):
    """Schema para retornar os dados de um usuário da API (sem a senha)."""
    id: int

    class Config:
        # Permite que o Pydantic mapeie os dados diretamente de um
        # modelo SQLAlchemy para este schema.
        from_attributes = True
