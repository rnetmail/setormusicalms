# fastapi_backend/crud/user.py
# Versão 72 18/07/2025 08:35
from sqlalchemy.orm import Session
from typing import Optional

# CORREÇÃO: As importações agora apontam para os pacotes corretos na raiz.
from models.user import User
from schemas.user import UserCreate, UserUpdate
from auth.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Busca um usuário pelo seu ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Busca um usuário pelo seu nome de usuário."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca um usuário pelo seu e-mail."""
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Retorna uma lista de usuários com paginação."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    """Cria um novo usuário, garantindo que a senha seja hasheada."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Atualiza um usuário existente. Se uma nova senha for fornecida, ela será hasheada."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        # Pydantic V2 usa .model_dump() em vez de .dict()
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> Optional[User]:
    """Deleta um usuário do banco de dados."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Autentica um usuário, verificando o nome de usuário e a senha hasheada."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
