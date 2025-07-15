# setormusicalms/backend/crud/repertorio_fixed.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from models.repertorio import RepertorioItem
from schemas.repertorio import RepertorioItemCreate, RepertorioItemUpdate

def get_repertorio_by_filters(
    db: Session,
    type_filter: Optional[str] = None,
    year_filter: Optional[str] = None,
    active_only: bool = True
):
    """
    Busca itens do repertório com base em filtros opcionais.
    """
    query = db.query(RepertorioItem)

    # Filtrar por tipo, se fornecido
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)

    # Filtrar por ano, se fornecido
    if year_filter:
        query = query.filter(RepertorioItem.year == year_filter)

    # Filtrar apenas por itens ativos. Comparar com '== True' é redundante.
    if active_only:
        query = query.filter(RepertorioItem.active)
    
    # Ordenar por ano (mais recente primeiro) e depois por título
    return query.order_by(RepertorioItem.year.desc(), RepertorioItem.title).all()

def create_repertorio_item(db: Session, item: RepertorioItemCreate):
    """
    Cria um novo item no repertório.
    """
    db_item = RepertorioItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_repertorio_item(db: Session, item_id: int, item: RepertorioItemUpdate):
    """
    Atualiza um item existente no repertório.
    """
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_repertorio_item(db: Session, item_id: int):
    """
    Deleta um item do repertório.
    """
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

def get_active_repertorio_by_group(db: Session, group_type: str):
    """
    Busca itens de repertório ativos para um grupo específico.
    """
    return db.query(RepertorioItem).filter(
        and_(
            RepertorioItem.type == group_type,
            # A forma idiomática de verificar um booleano é usar o próprio valor
            RepertorioItem.active
        )
    ).order_by(RepertorioItem.year.desc(), RepertorioItem.title).all()
