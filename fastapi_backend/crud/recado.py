# /fastapi_backend/crud/recado.py
# v2.0 - 2025-07-30 23:12:00 - Corrige importações para estrutura correta do projeto.

from sqlalchemy.orm import Session
from typing import List, Optional

from models.recado import RecadoItem
from schemas.recado import RecadoItemCreate, RecadoItemUpdate

def get_recado(db: Session, recado_id: int) -> Optional[RecadoItem]:
    """Busca um recado específico pelo seu ID."""
    return db.query(RecadoItem).filter(RecadoItem.id == recado_id).first()

def get_recados(db: Session, skip: int = 0, limit: int = 100) -> List[RecadoItem]:
    """Lista todos os recados com paginação."""
    return db.query(RecadoItem).offset(skip).limit(limit).all()

def create_recado(db: Session, recado: RecadoItemCreate, user_id: int) -> RecadoItem:
    """Cria um novo recado no banco de dados."""
    db_recado = RecadoItem(**recado.model_dump(), owner_id=user_id)
    db.add(db_recado)
    db.commit()
    db.refresh(db_recado)
    return db_recado

def update_recado(db: Session, recado_id: int, recado_update: RecadoItemUpdate) -> Optional[RecadoItem]:
    """Atualiza um recado existente."""
    db_recado = get_recado(db, recado_id)
    if db_recado:
        update_data = recado_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recado, field, value)
        db.commit()
        db.refresh(db_recado)
    return db_recado

def delete_recado(db: Session, recado_id: int) -> bool:
    """Deleta um recado do banco de dados."""
    db_recado = get_recado(db, recado_id)
    if db_recado:
        db.delete(db_recado)
        db.commit()
        return True
    return False

