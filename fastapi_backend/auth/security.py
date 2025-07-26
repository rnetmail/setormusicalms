# fastapi_backend/auth/security.py
# Versão 05 - FINAL E COMPLETA

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.database import get_db
from models import user as model_user
from schemas import token as schema_token
from crud import user as crud_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[model_user.User]:
    """
    Verifica se um usuário existe e se a senha está correta.
    Retorna o objeto do usuário em caso de sucesso, ou None caso contrário.
    """
    user = crud_user.get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> model_user.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema_token.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: model_user.User = Depends(get_current_user),
) -> model_user.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user

def get_current_staff_user(
    current_user: model_user.User = Depends(get_current_active_user),
) -> model_user.User:
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não tem permissões de administrador",
        )
    return current_user

def get_current_superuser(
    current_user: model_user.User = Depends(get_current_staff_user),
) -> model_user.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ação restrita a superusuários",
        )
    return current_user
