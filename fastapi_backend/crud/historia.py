# /fastapi_backend/crud/historia.py
# v2.0 - 2025-07-30 23:14:00 - Corrige importações para estrutura correta do projeto.

from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.historia import HistoriaItem
from ..schemas.historia import HistoriaItemCreate, HistoriaItemUpdate

def get_historia(db: Session, historia_id: int) -> Optional[HistoriaItem]:
    """Busca um item da história específico pelo seu ID."""
    return db.query(HistoriaItem).filter(HistoriaItem.id == historia_id).first()

def get_historias(db: Session, skip: int = 0, limit: int = 100) -> List[HistoriaItem]:
    """Lista todos os itens da história com paginação."""
    return db.query(HistoriaItem).offset(skip).limit(limit).all()

def create_historia(db: Session, historia: HistoriaItemCreate) -> HistoriaItem:
    """Cria um novo item da história no banco de dados."""
    db_historia = HistoriaItem(**historia.model_dump())
    db.add(db_historia)
    db.commit()
    db.refresh(db_historia)
    return db_historia

def update_historia(db: Session, historia_id: int, historia_update: HistoriaItemUpdate) -> Optional[HistoriaItem]:
    """Atualiza um item da história existente."""
    db_historia = get_historia(db, historia_id)
    if db_historia:
        update_data = historia_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_historia, field, value)
        db.commit()
        db.refresh(db_historia)
    return db_historia

def delete_historia(db: Session, historia_id: int) -> bool:
    """Deleta um item da história do banco de dados."""
    db_historia = get_historia(db, historia_id)
    if db_historia:
        db.delete(db_historia)
        db.commit()
        return True
    return False

