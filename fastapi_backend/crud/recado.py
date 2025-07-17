# fastapi_backend/crud/recado.py
# Versão 77 18/07/2025 08:49
from sqlalchemy.orm import Session
from typing import List, Optional

# CORREÇÃO: As importações agora apontam para os pacotes corretos na raiz.
from models.recado import RecadoItem
from schemas.recado import RecadoItemCreate, RecadoItemUpdate

def get_recado_item(db: Session, item_id: int) -> Optional[RecadoItem]:
    """Busca um recado específico pelo ID."""
    return db.query(RecadoItem).filter(RecadoItem.id == item_id).first()

def get_recado_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    group_filter: Optional[str] = None,
    active_only: bool = True
) -> List[RecadoItem]:
    """
    Lista recados com filtros opcionais para grupo e status.
    Os resultados são ordenados por data (mais recente primeiro).
    """
    query = db.query(RecadoItem)
    
    if group_filter:
        query = query.filter(RecadoItem.group == group_filter)
    
    if active_only:
        query = query.filter(RecadoItem.active == True)

    return query.order_by(RecadoItem.date.desc()).offset(skip).limit(limit).all()

def create_recado_item(db: Session, item: RecadoItemCreate) -> RecadoItem:
    """Cria um novo recado."""
    db_item = RecadoItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_recado_item(db: Session, item_id: int, item_update: RecadoItemUpdate) -> Optional[RecadoItem]:
    """Atualiza um recado."""
    db_item = db.query(RecadoItem).filter(RecadoItem.id == item_id).first()
    if db_item:
        update_data = item_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_recado_item(db: Session, item_id: int) -> Optional[RecadoItem]:
    """Remove um recado do banco de dados."""
    db_item = db.query(RecadoItem).filter(RecadoItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
