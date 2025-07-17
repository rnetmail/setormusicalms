# fastapi_backend/app/routers/agenda.py
# Versão 56 18/07/2025 00:03
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

# CORREÇÃO: Importações diretas dos pacotes a partir da raiz do projeto
import crud
import models
import schemas
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user

router = APIRouter(prefix="/agenda")

@router.get("/", response_model=List[schemas.agenda.AgendaItem])
def read_agenda_items(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filtrar por grupo: Coral, Orquestra, ou Setor"),
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint para listar os itens da agenda com filtros e paginação."""
    items = crud.agenda.get_agenda_items(db, skip=skip, limit=limit, group_filter=group_filter)
    return items

@router.post("/", response_model=schemas.agenda.AgendaItem, status_code=201)
def create_agenda_item_endpoint(
    item: schemas.agenda.AgendaItemCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para criar um novo item na agenda."""
    return crud.agenda.create_agenda_item(db=db, item=item)

@router.get("/{item_id}", response_model=schemas.agenda.AgendaItem)
def read_agenda_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint para obter um item da agenda específico pelo ID."""
    db_item = crud.agenda.get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schemas.agenda.AgendaItem)
def update_agenda_item_endpoint(
    item_id: int,
    item_update: schemas.agenda.AgendaItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para atualizar um item da agenda."""
    db_item = crud.agenda.update_agenda_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado.")
    return db_item

@router.delete("/{item_id}", status_code=204)
def delete_agenda_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para apagar um item da agenda."""
    db_item = crud.agenda.delete_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado.")
    return
