# /fastapi_backend/crud/agenda.py
# v2.0 - 2025-07-30 23:13:00 - Corrige importações para estrutura correta do projeto.

from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.agenda import AgendaItem
from ..schemas.agenda import AgendaItemCreate, AgendaItemUpdate

def get_agenda_item(db: Session, item_id: int) -> Optional[AgendaItem]:
    """Busca um item da agenda específico pelo seu ID."""
    return db.query(AgendaItem).filter(AgendaItem.id == item_id).first()

def get_agenda_items(db: Session, skip: int = 0, limit: int = 100) -> List[AgendaItem]:
    """Lista todos os itens da agenda com paginação."""
    return db.query(AgendaItem).offset(skip).limit(limit).all()

def create_agenda_item(db: Session, item: AgendaItemCreate) -> AgendaItem:
    """Cria um novo item da agenda no banco de dados."""
    db_item = AgendaItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_agenda_item(db: Session, item_id: int, item_update: AgendaItemUpdate) -> Optional[AgendaItem]:
    """Atualiza um item da agenda existente."""
    db_item = get_agenda_item(db, item_id)
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_agenda_item(db: Session, item_id: int) -> bool:
    """Deleta um item da agenda do banco de dados."""
    db_item = get_agenda_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

