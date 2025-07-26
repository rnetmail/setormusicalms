# fastapi_backend/app/routers/historia.py
# Versão 01 25/07/2025 14:22
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from auth.security import get_current_staff_user
from crud import historia as crud_historia
from models import user as model_user
from schemas import historia as schema_historia

router = APIRouter(prefix="/historia", tags=["História"])

@router.get("/", response_model=List[schema_historia.HistoriaItem])
def read_historia_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os itens da história. Acesso público."""
    items = crud_historia.get_historia_items(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schema_historia.HistoriaItem, status_code=status.HTTP_201_CREATED)
def create_historia_item(
    item: schema_historia.HistoriaItemCreate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Cria um novo item na história. Apenas para staff."""
    return crud_historia.create_historia_item(db=db, item=item)

@router.get("/{item_id}", response_model=schema_historia.HistoriaItem)
def read_historia_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Obtém um item específico da história pelo ID. Acesso público."""
    db_item = crud_historia.get_historia_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da história não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schema_historia.HistoriaItem)
def update_historia_item(
    item_id: int,
    item_update: schema_historia.HistoriaItemUpdate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Atualiza um item da história. Apenas para staff."""
    db_item = crud_historia.update_historia_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da história não encontrado para atualização.")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_historia_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Apaga um item da história. Apenas para staff."""
    db_item = crud_historia.delete_historia_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da história não encontrado para exclusão.")
    return
