# fastapi_backend/crud/historia.py
# Versão 01 25/07/2025 13:53
from sqlalchemy.orm import Session
from typing import List, Optional

from models.historia import HistoriaItem
from schemas.historia import HistoriaItemCreate, HistoriaItemUpdate

def get_historia_item(db: Session, item_id: int) -> Optional[HistoriaItem]:
    """Busca um item da história específico pelo seu ID."""
    return db.query(HistoriaItem).filter(HistoriaItem.id == item_id).first()

def get_historia_items(db: Session, skip: int = 0, limit: int = 100) -> List[HistoriaItem]:
    """Lista todos os itens da história com paginação, ordenados por ano."""
    return db.query(HistoriaItem).order_by(HistoriaItem.year).offset(skip).limit(limit).all()

def create_historia_item(db: Session, item: HistoriaItemCreate) -> HistoriaItem:
    """Cria um novo item na história."""
    db_item = HistoriaItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_historia_item(db: Session, item_id: int, item_update: HistoriaItemUpdate) -> Optional[HistoriaItem]:
    """Atualiza um item da história existente."""
    db_item = db.query(HistoriaItem).filter(HistoriaItem.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_historia_item(db: Session, item_id: int) -> Optional[HistoriaItem]:
    """Remove um item da história do banco de dados."""
    db_item = db.query(HistoriaItem).filter(HistoriaItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
