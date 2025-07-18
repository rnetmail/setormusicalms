# fastapi_backend/auth/security.py
# Versão 87 18/07/2025 10:08
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import crud
import models
import schemas
from app.config import settings
from app.database import get_db
# A importação das funções de senha foi removida daqui.

# O tokenUrl deve corresponder ao endpoint de login completo.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo token de acesso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.user.User:
    """
    Dependência que decodifica o token JWT, extrai o nome de usuário e busca o usuário no banco de dados.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.user.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = crud.user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: models.user.User = Depends(get_current_user)) -> models.user.User:
    """Dependência que garante que o usuário obtido do token está ativo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


def get_current_staff_user(current_user: models.user.User = Depends(get_current_active_user)) -> models.user.User:
    """Dependência que garante que o usuário é um membro da equipe (staff) ou superusuário."""
    if not current_user.is_staff and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissão de staff"
        )
    return current_user


def get_current_superuser(current_user: models.user.User = Depends(get_current_active_user)) -> models.user.User:
    """Dependência que garante que o usuário é um superusuário."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissão de superusuário"
        )
    return current_user
