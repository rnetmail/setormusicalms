# fastapi_backend/crud/agenda.py
# Versão 24 18/07/2025 00:20
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações absolutas a partir da raiz do pacote 'fastapi_backend'
from models.agenda import AgendaItem
from schemas.agenda import AgendaItemCreate, AgendaItemUpdate

def get_agenda_item(db: Session, item_id: int) -> Optional[AgendaItem]:
    """Busca um item da agenda específico pelo seu ID."""
    return db.query(AgendaItem).filter(AgendaItem.id == item_id).first()

def get_agenda_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    group_filter: Optional[str] = None,
    active_only: bool = True
) -> List[AgendaItem]:
    """
    Lista os itens da agenda, com filtros opcionais para grupo e status, e com paginação.
    Os resultados são ordenados por data (mais recente primeiro).
    """
    query = db.query(AgendaItem)
    
    if group_filter:
        query = query.filter(AgendaItem.group == group_filter)

    if active_only:
        query = query.filter(AgendaItem.active == True)
    
    return query.order_by(AgendaItem.date.desc()).offset(skip).limit(limit).all()

def create_agenda_item(db: Session, item: AgendaItemCreate) -> AgendaItem:
    """Cria um novo item na agenda."""
    db_item = AgendaItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_agenda_item(db: Session, item_id: int, item_update: AgendaItemUpdate) -> Optional[AgendaItem]:
    """Atualiza um item da agenda existente."""
    db_item = db.query(AgendaItem).filter(AgendaItem.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_agenda_item(db: Session, item_id: int) -> Optional[AgendaItem]:
    """Remove um item da agenda do banco de dados."""
    db_item = db.query(AgendaItem).filter(AgendaItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
