# fastapi_backend/crud/user.py
# Versão 04 - FINAL E COMPLETA

from sqlalchemy.orm import Session
from typing import List, Optional

from models import user as model_user
from schemas import user as schema_user
# CORREÇÃO DEFINITIVA: Importa a função de hashing do novo módulo 'auth.hashing',
# quebrando a dependência circular com 'auth.security'.
from auth.hashing import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[model_user.User]:
    """Busca um usuário específico pelo seu ID."""
    return db.query(model_user.User).filter(model_user.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[model_user.User]:
    """Busca um usuário específico pelo seu nome de usuário."""
    return db.query(model_user.User).filter(model_user.User.username == username).first()

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

def update_user(db: Session, user_id: int, user_update: schema_user.UserUpdate) -> Optional[model_user.User]:
    """Atualiza um usuário existente."""
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        # Se uma nova senha for fornecida, gera o hash dela.
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
