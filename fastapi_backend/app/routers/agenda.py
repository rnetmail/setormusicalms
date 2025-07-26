# fastapi_backend/app/routers/agenda.py
# Versão 01 25/07/2025 14:18
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from auth.security import get_current_staff_user
from crud import agenda as crud_agenda
from models import user as model_user
from schemas import agenda as schema_agenda

router = APIRouter(prefix="/agenda", tags=["Agenda"])

@router.get("/", response_model=List[schema_agenda.AgendaItem])
def read_agenda_items(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filtrar por grupo: Coral, Orquestra, ou Setor"),
    db: Session = Depends(get_db)
):
    """Lista os itens da agenda com filtros e paginação. Acesso público."""
    items = crud_agenda.get_agenda_items(db, skip=skip, limit=limit, group_filter=group_filter)
    return items

@router.post("/", response_model=schema_agenda.AgendaItem, status_code=status.HTTP_201_CREATED)
def create_agenda_item(
    item: schema_agenda.AgendaItemCreate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Cria um novo item na agenda. Apenas para staff."""
    return crud_agenda.create_agenda_item(db=db, item=item)

@router.get("/{item_id}", response_model=schema_agenda.AgendaItem)
def read_agenda_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Obtém um item da agenda específico pelo ID. Acesso público."""
    db_item = crud_agenda.get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schema_agenda.AgendaItem)
def update_agenda_item(
    item_id: int,
    item_update: schema_agenda.AgendaItemUpdate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Atualiza um item da agenda. Apenas para staff."""
    db_item = crud_agenda.update_agenda_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado para atualização.")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agenda_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Apaga um item da agenda. Apenas para staff."""
    db_item = crud_agenda.delete_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado para exclusão.")
    return
