# fastapi_backend/crud/recado.py
# Versão 11 17/07/2025 17:10
from sqlalchemy.orm import Session
from typing import List, Optional

from models.recado import RecadoItem
from schemas.recado import RecadoItemCreate, RecadoItemUpdate

def get_recado_item(db: Session, item_id: int) -> Optional[RecadoItem]:
    """
    Busca um recado específico pelo seu ID.

    Args:
        db: A sessão do banco de dados.
        item_id: O ID do recado a ser buscado.

    Returns:
        O objeto RecadoItem se encontrado, caso contrário None.
    """
    return db.query(RecadoItem).filter(RecadoItem.id == item_id).first()

def get_recado_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    group_filter: Optional[str] = None,
    active_only: bool = True
) -> List[RecadoItem]:
    """
    Lista os recados, com filtros e paginação.

    Args:
        db: A sessão do banco de dados.
        skip: O número de registros a pular (para paginação).
        limit: O número máximo de registros a retornar.
        group_filter: Filtra os resultados por grupo (ex: 'Coral', 'Orquestra').
        active_only: Se True, retorna apenas os recados ativos.

    Returns:
        Uma lista de objetos RecadoItem.
    """
    query = db.query(RecadoItem)
    
    if group_filter:
        query = query.filter(RecadoItem.group == group_filter)
    
    if active_only:
        query = query.filter(RecadoItem.active == True)

    return query.order_by(RecadoItem.date.desc()).offset(skip).limit(limit).all()

def create_recado_item(db: Session, item: RecadoItemCreate) -> RecadoItem:
    """Cria um novo recado no banco de dados."""
    db_item = RecadoItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_recado_item(db: Session, item_id: int, item_update: RecadoItemUpdate) -> Optional[RecadoItem]:
    """Atualiza um recado existente."""
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
