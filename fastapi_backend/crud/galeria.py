# fastapi_backend/crud/galeria.py
# Versão 01 25/07/2025 14:00
from sqlalchemy.orm import Session
from typing import List, Optional

from models.galeria import GaleriaItem
from schemas.galeria import GaleriaItemCreate, GaleriaItemUpdate

def get_galeria_item(db: Session, item_id: int) -> Optional[GaleriaItem]:
    """Busca um item da galeria específico pelo seu ID."""
    return db.query(GaleriaItem).filter(GaleriaItem.id == item_id).first()

def get_galeria_items_by_group(db: Session, group: str, skip: int = 0, limit: int = 100) -> List[GaleriaItem]:
    """Lista todos os itens da galeria para um grupo específico, com paginação."""
    return db.query(GaleriaItem).filter(GaleriaItem.group == group).order_by(GaleriaItem.date.desc()).offset(skip).limit(limit).all()

def create_galeria_item(db: Session, item: GaleriaItemCreate) -> GaleriaItem:
    """Cria um novo item na galeria."""
    db_item = GaleriaItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_galeria_item(db: Session, item_id: int, item_update: GaleriaItemUpdate) -> Optional[GaleriaItem]:
    """Atualiza um item da galeria existente."""
    db_item = db.query(GaleriaItem).filter(GaleriaItem.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_galeria_item(db: Session, item_id: int) -> Optional[GaleriaItem]:
    """Remove um item da galeria do banco de dados."""
    db_item = db.query(GaleriaItem).filter(GaleriaItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
