# fastapi_backend/schemas/user.py
# Versão 01 25/07/2025 11:01
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Schema base com os campos comuns de um usuário."""
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

class UserCreate(UserBase):
    """Schema para a criação de um novo usuário, exigindo a senha."""
    password: str

class UserUpdate(BaseModel):
    """Schema para atualização de um usuário. Todos os campos são opcionais."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = None

class User(UserBase):
    """Schema para retornar os dados de um usuário da API (sem a senha)."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # Permite que o Pydantic mapeie os dados diretamente de um modelo SQLAlchemy.
        from_attributes = True
