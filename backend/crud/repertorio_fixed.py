from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from models.repertorio import RepertorioItem
from schemas.repertorio import RepertorioItemCreate, RepertorioItemUpdate
from utils.media_converter import process_media_urls, validate_media_urls

def get_repertorio_item(db: Session, item_id: int):
    """Busca um item específico do repertório"""
    return db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()

def get_repertorio_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    type_filter: Optional[str] = None,
    active_only: bool = True
):
    """Lista itens do repertório com filtros"""
    query = db.query(RepertorioItem)
    
    # Filtrar por tipo (Coral, Orquestra, Setor)
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)
    
    # Filtrar apenas ativos
    if active_only:
        query = query.filter(RepertorioItem.active == True)
    
    # Ordenar por ano e título
    query = query.order_by(RepertorioItem.year.desc(), RepertorioItem.title)
    
    return query.offset(skip).limit(limit).all()

def create_repertorio_item(db: Session, item: RepertorioItemCreate):
    """Cria um novo item do repertório"""
    # Converter para dict
    item_data = item.dict()
    
    # Validar URLs de mídia
    errors = validate_media_urls(item_data)
    if errors:
        raise ValueError(f"Erros de validação: {', '.join(errors)}")
    
    # Processar URLs de mídia
    processed_data = process_media_urls(item_data)
    
    # Criar item no banco
    db_item = RepertorioItem(**processed_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_repertorio_item(db: Session, item_id: int, item_update: RepertorioItemUpdate):
    """Atualiza um item do repertório"""
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if not db_item:
        return None
    
    # Converter para dict, excluindo valores None
    update_data = item_update.dict(exclude_unset=True)
    
    # Validar URLs de mídia se fornecidas
    if any(key in update_data for key in ["audio_url", "video_url", "sheet_music_url"]):
        # Combinar dados existentes com atualizações para validação completa
        full_data = {
            "audio_url": getattr(db_item, "audio_url", ""),
            "video_url": getattr(db_item, "video_url", ""),
            "sheet_music_url": getattr(db_item, "sheet_music_url", "")
        }
        full_data.update(update_data)
        
        errors = validate_media_urls(full_data)
        if errors:
            raise ValueError(f"Erros de validação: {', '.join(errors)}")
        
        # Processar URLs de mídia
        processed_data = process_media_urls(update_data)
        update_data = processed_data
    
    # Atualizar campos
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_repertorio_item(db: Session, item_id: int):
    """Remove um item do repertório"""
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if not db_item:
        return None
    
    db.delete(db_item)
    db.commit()
    return db_item

def get_repertorio_by_group_and_year(
    db: Session, 
    group_type: str, 
    year: Optional[int] = None
):
    """Busca repertório por grupo e ano"""
    query = db.query(RepertorioItem).filter(
        and_(
            RepertorioItem.type == group_type,
            RepertorioItem.active == True
        )
    )
    
    if year:
        query = query.filter(RepertorioItem.year == year)
    
    return query.order_by(RepertorioItem.title).all()

def get_available_years(db: Session, group_type: Optional[str] = None):
    """Retorna anos disponíveis no repertório"""
    query = db.query(RepertorioItem.year).distinct()
    
    if group_type:
        query = query.filter(RepertorioItem.type == group_type)
    
    years = [year[0] for year in query.all() if year[0]]
    return sorted(years, reverse=True)

