# fastapi_backend/app/routers/repertorio.py
# Versão 64 18/07/2025 00:22
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import crud
import models
import schemas
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user

router = APIRouter(prefix="/repertorio")

@router.get("/", response_model=List[schemas.repertorio.RepertorioItem])
def read_repertorio_items(
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None, description="Filtrar por tipo: Coral ou Orquestra"),
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint para listar os itens do repertório com filtros e paginação."""
    items = crud.repertorio.get_repertorio_items(db, skip=skip, limit=limit, type_filter=type_filter)
    return items

@router.post("/", response_model=schemas.repertorio.RepertorioItem, status_code=201)
def create_repertorio_item_endpoint(
    item: schemas.repertorio.RepertorioItemCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para criar um novo item de repertório."""
    return crud.repertorio.create_repertorio_item(db=db, item=item)

@router.get("/{item_id}", response_model=schemas.repertorio.RepertorioItem)
def read_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint para obter um item de repertório específico pelo ID."""
    db_item = crud.repertorio.get_repertorio_item(db, item_id=item_id)
    # CORREÇÃO: A linha estava incompleta.
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schemas.repertorio.RepertorioItem)
def update_repertorio_item_endpoint(
    item_id: int,
    item_update: schemas.repertorio.RepertorioItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para atualizar um item de repertório."""
    db_item = crud.repertorio.update_repertorio_item(db, item_id=item_id, item_update=item_update)
    # CORREÇÃO: A linha estava incompleta.
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado.")
    return db_item

@router.delete("/{item_id}", status_code=204)
def delete_repertorio_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para apagar um item de repertório."""
    db_item = crud.repertorio.delete_repertorio_item(db, item_id=item_id)
    # CORREÇÃO: A linha estava incompleta.
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado.")
    return
