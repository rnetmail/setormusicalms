# /fastapi_backend/crud/galeria.py
# v3.0 - 2025-08-08 - Final, com importações diretas para estrutura simplificada.

from sqlalchemy.orm import Session
from typing import List, Optional

# --- CORRETO ---
from models.galeria import GaleriaItem
from schemas.galeria import GaleriaItemCreate, GaleriaItemUpdate

# ... (resto do código está correto)
def get_galeria_item(db: Session, item_id: int) -> Optional[GaleriaItem]:
    """Busca um item da galeria específico pelo seu ID."""
    return db.query(GaleriaItem).filter(GaleriaItem.id == item_id).first()

def get_galeria_items(db: Session, skip: int = 0, limit: int = 100) -> List[GaleriaItem]:
    """Lista todos os itens da galeria com paginação."""
    return db.query(GaleriaItem).order_by(GaleriaItem.id.desc()).offset(skip).limit(limit).all()

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
