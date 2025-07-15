# setormusicalms/backend/app/main_production.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from models.repertorio import RepertorioItem
from models.agenda import AgendaItem
from models.recado import RecadoItem
# Using aliases to prevent name conflicts between models and schemas
from schemas.repertorio import RepertorioItem as RepertorioItemSchema
from schemas.agenda import AgendaItem as AgendaItemSchema
from schemas.recado import RecadoItem as RecadoItemSchema

router = APIRouter()

# --- Repertorio Endpoints ---

@router.get("/repertorio/all", response_model=List[RepertorioItemSchema])
def get_all_repertorio(
    type_filter: Optional[str] = None,
    year_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Gets all active repertoire items, with optional filters for type and year.
    """
    query = db.query(RepertorioItem).filter(RepertorioItem.active)
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)
    if year_filter:
        query = query.filter(RepertorioItem.year == year_filter)
    
    return query.order_by(RepertorioItem.year.desc(), RepertorioItem.title).all()

# --- Agenda Endpoints ---

@router.get("/agenda/all", response_model=List[AgendaItemSchema])
def get_all_agenda(
    group_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Gets all active agenda items, with an optional filter for a group.
    """
    query = db.query(AgendaItem).filter(AgendaItem.active)
    if group_filter:
        query = query.filter(AgendaItem.group == group_filter)
    
    return query.order_by(AgendaItem.date.desc()).all()

@router.get("/agenda/{group_type}", response_model=List[AgendaItemSchema])
def get_agenda_by_group(group_type: str, db: Session = Depends(get_db)):
    """
    Gets all active agenda items for a specific group.
    """
    return db.query(AgendaItem).filter(
        AgendaItem.group == group_type,
        AgendaItem.active
    ).order_by(AgendaItem.date.desc()).all()

# --- Recados (Messages) Endpoints ---

@router.get("/recados/all", response_model=List[RecadoItemSchema])
def get_all_recados(
    group_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Gets all active messages (recados), with an optional filter for a group.
    """
    query = db.query(RecadoItem).filter(RecadoItem.active)
    if group_filter:
        query = query.filter(RecadoItem.group == group_filter)
    
    return query.order_by(RecadoItem.date.desc()).all()

@router.get("/recados/{group_type}", response_model=List[RecadoItemSchema])
def get_recados_by_group(group_type: str, db: Session = Depends(get_db)):
    """
    Gets all active messages (recados) for a specific group.
    """
    return db.query(RecadoItem).filter(
        RecadoItem.group == group_type,
        RecadoItem.active
    ).order_by(RecadoItem.date.desc()).all()
