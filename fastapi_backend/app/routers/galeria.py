# fastapi_backend/app/routers/galeria.py
# Versão 01 25/07/2025 14:25
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.database import get_db
from auth.security import get_current_staff_user
from crud import galeria as crud_galeria
from models import user as model_user
from schemas import galeria as schema_galeria

router = APIRouter(prefix="/galeria", tags=["Galeria"])

@router.get("/{group}", response_model=List[schema_galeria.GaleriaItem])
def read_galeria_items_by_group(
    group: str = Path(..., description="Filtrar por grupo: Coral ou Orquestra"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista os itens da galeria de um grupo específico. Acesso público."""
    if group not in ["Coral", "Orquestra"]:
        raise HTTPException(status_code=400, detail="O grupo deve ser 'Coral' ou 'Orquestra'")
    items = crud_galeria.get_galeria_items_by_group(db, group=group, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schema_galeria.GaleriaItem, status_code=status.HTTP_201_CREATED)
def create_galeria_item(
    item: schema_galeria.GaleriaItemCreate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Cria um novo item na galeria. Apenas para staff."""
    return crud_galeria.create_galeria_item(db=db, item=item)

@router.put("/{item_id}", response_model=schema_galeria.GaleriaItem)
def update_galeria_item(
    item_id: int,
    item_update: schema_galeria.GaleriaItemUpdate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Atualiza um item da galeria. Apenas para staff."""
    db_item = crud_galeria.update_galeria_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da galeria não encontrado para atualização.")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_galeria_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Apaga um item da galeria. Apenas para staff."""
    db_item = crud_galeria.delete_galeria_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da galeria não encontrado para exclusão.")
    return
