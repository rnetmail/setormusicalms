# fastapi_backend/crud/user.py
# Versão 01 25/07/2025 11:20
from sqlalchemy.orm import Session
from typing import Optional

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..auth.password import get_password_hash, verify_password

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Busca um usuário específico pelo ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Busca um usuário específico pelo nome de usuário."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca um usuário específico pelo e-mail."""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Lista todos os usuários com paginação."""
    return db.query(User).offset
