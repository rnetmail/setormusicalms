# fastapi_backend/app/routers/recados.py
# Versão 57 18/07/2025 00:04
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

# CORREÇÃO: Importações diretas dos pacotes a partir da raiz do projeto
import crud
import models
import schemas
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user

router = APIRouter(prefix="/recados")

@router.get("/", response_model=List[schemas.recado.RecadoItem])
def read_recado_items(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filtrar por grupo: Coral, Orquestra, ou Setor"),
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint para listar os recados com filtros e paginação."""
    items = crud.recado.get_recado_items(db, skip=skip, limit=limit, group_filter=group_filter)
    return items

@router.post("/", response_model=schemas.recado.RecadoItem, status_code=201)
def create_recado_item_endpoint(
    item: schemas.recado.RecadoItemCreate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para criar um novo recado."""
    return crud.recado.create_recado_item(db=db, item=item)

@router.get("/{item_id}", response_model=schemas.recado.RecadoItem)
def read_recado_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Endpoint para obter um recado específico pelo ID."""
    db_item = crud.recado.get_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schemas.recado.RecadoItem)
def update_recado_item_endpoint(
    item_id: int,
    item_update: schemas.recado.RecadoItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para atualizar um recado."""
    db_item = crud.recado.update_recado_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado.")
    return db_item

@router.delete("/{item_id}", status_code=204)
def delete_recado_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Endpoint para apagar um recado."""
    db_item = crud.recado.delete_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado.")
    return
