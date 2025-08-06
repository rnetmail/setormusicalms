# /fastapi_backend/crud/galeria.py
# v2.0 - 2025-07-30 23:15:00 - Corrige importações para estrutura correta do projeto.

from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.galeria import GaleriaItem
from ..schemas.galeria import GaleriaItemCreate, GaleriaItemUpdate

def get_galeria_item(db: Session, item_id: int) -> Optional[GaleriaItem]:
    """Busca um item da galeria específico pelo seu ID."""
    return db.query(GaleriaItem).filter(GaleriaItem.id == item_id).first()

def get_galeria_items(db: Session, skip: int = 0, limit: int = 100) -> List[GaleriaItem]:
    """Lista todos os itens da galeria com paginação."""
    return db.query(GaleriaItem).offset(skip).limit(limit).all()

def create_galeria_item(db: Session, item: GaleriaItemCreate) -> GaleriaItem:
    """Cria um novo item da galeria no banco de dados."""
    db_item = GaleriaItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_galeria_item(db: Session, item_id: int, item_update: GaleriaItemUpdate) -> Optional[GaleriaItem]:
    """Atualiza um item da galeria existente."""
    db_item = get_galeria_item(db, item_id)
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_galeria_item(db: Session, item_id: int) -> bool:
    """Deleta um item da galeria do banco de dados."""
    db_item = get_galeria_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

