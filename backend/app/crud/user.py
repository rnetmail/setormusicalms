# setormusicalms/backend/crud/user.py
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from auth.security import get_password_hash

def get_user(db: Session, user_id: int):
    """Busca um usuário pelo seu ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Busca um usuário pelo seu nome de usuário."""
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Busca uma lista de usuários, com suporte para paginação."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """Cria um novo usuário no banco de dados com uma senha hasheada."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        active=user.active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Atualiza os dados de um usuário existente."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Se uma nova senha for fornecida, faz o hash dela
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        update_data["hashed_password"] = hashed_password
        del update_data["password"] # Remove a senha em texto plano
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Deleta um usuário do banco de dados."""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
