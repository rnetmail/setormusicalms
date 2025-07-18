# fastapi_backend/crud/repertorio.py
# Versão 12 17/07/2025 23:57
from sqlalchemy.orm import Session
from typing import List, Optional

# Importações absolutas a partir da raiz do pacote 'fastapi_backend'
from models.repertorio import RepertorioItem
from schemas.repertorio import RepertorioItemCreate, RepertorioItemUpdate
from utils.media_converter import process_media_urls

def get_repertorio_item(db: Session, item_id: int) -> Optional[RepertorioItem]:
    """Busca um item de repertório específico pelo ID."""
    return db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()

def get_repertorio_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    type_filter: Optional[str] = None,
    active_only: bool = True
) -> List[RepertorioItem]:
    """
    Lista itens do repertório com filtros e paginação.
    Os resultados são ordenados por ano (mais recente primeiro) e depois por título.
    """
    query = db.query(RepertorioItem)
    
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)
    
    if active_only:
        query = query.filter(RepertorioItem.active == True)
    
    return query.order_by(RepertorioItem.year.desc(), RepertorioItem.title).offset(skip).limit(limit).all()

def create_repertorio_item(db: Session, item: RepertorioItemCreate) -> RepertorioItem:
    """Cria um novo item de repertório, processando as URLs de mídia antes de salvar."""
    item_data = item.model_dump()
    
    # Converte as URLs de mídia para formatos adequados (download direto, embed, etc.)
    processed_data = process_media_urls(item_data)
    
    db_item = RepertorioItem(**processed_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_repertorio_item(db: Session, item_id: int, item_update: RepertorioItemUpdate) -> Optional[RepertorioItem]:
    """Atualiza um item de repertório, processando as URLs de mídia se forem alteradas."""
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if not db_item:
        return None
    
    update_data = item_update.model_dump(exclude_unset=True)
    
    # Processa as URLs de mídia apenas se elas estiverem presentes nos dados de atualização.
    processed_update_data = process_media_urls(update_data)
    
    for field, value in processed_update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_repertorio_item(db: Session, item_id: int) -> Optional[RepertorioItem]:
    """Remove um item de repertório do banco de dados."""
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
