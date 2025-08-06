# /fastapi_backend/crud/repertorio.py
# v2.0 - 2025-07-30 23:16:00 - Corrige importações para estrutura correta do projeto.

from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.repertorio import RepertorioItem
from ..schemas.repertorio import RepertorioItemCreate, RepertorioItemUpdate

def get_repertorio_item(db: Session, item_id: int) -> Optional[RepertorioItem]:
    """Busca um item do repertório específico pelo seu ID."""
    return db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()

def get_repertorio_items(db: Session, skip: int = 0, limit: int = 100) -> List[RepertorioItem]:
    """Lista todos os itens do repertório com paginação."""
    return db.query(RepertorioItem).offset(skip).limit(limit).all()

def create_repertorio_item(db: Session, item: RepertorioItemCreate) -> RepertorioItem:
    """Cria um novo item do repertório no banco de dados."""
    db_item = RepertorioItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_repertorio_item(db: Session, item_id: int, item_update: RepertorioItemUpdate) -> Optional[RepertorioItem]:
    """Atualiza um item do repertório existente."""
    db_item = get_repertorio_item(db, item_id)
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_repertorio_item(db: Session, item_id: int) -> bool:
    """Deleta um item do repertório do banco de dados."""
    db_item = get_repertorio_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

