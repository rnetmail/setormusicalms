# /fastapi_backend/crud/user.py
# v2.0 - 2025-07-30 23:08:00 - Corrige importações para estrutura correta do projeto.

from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models import user as model_user
from schemas import user as schema_user
from auth.hashing import get_password_hash, verify_password
from auth.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_user(db: Session, user_id: int) -> Optional[model_user.User]:
    """Busca um usuário específico pelo seu ID."""
    return db.query(model_user.User).filter(model_user.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[model_user.User]:
    """Busca um usuário específico pelo seu nome de usuário."""
    return db.query(model_user.User).filter(model_user.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[model_user.User]:
    """Busca um usuário específico pelo seu email."""
    return db.query(model_user.User).filter(model_user.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[model_user.User]:
    """Lista todos os usuários com paginação."""
    return db.query(model_user.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema_user.UserCreate) -> model_user.User:
    """Cria um novo usuário no banco de dados com a senha hasheada."""
    hashed_password = get_password_hash(user.password)
    db_user = model_user.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[model_user.User]:
    """Autentica um usuário verificando username e senha."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(db: Session, token: str = Depends(oauth2_scheme)) -> model_user.User:
    """Obtém o usuário atual a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: model_user.User = Depends(get_current_user)) -> model_user.User:
    """Verifica se o usuário atual está ativo."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def update_user(db: Session, user_id: int, user_update: schema_user.UserUpdate) -> Optional[model_user.User]:
    """Atualiza um usuário existente."""
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Deleta um usuário do banco de dados."""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

