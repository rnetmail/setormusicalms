from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user
from crud.recado import (
    get_recado_item, get_recado_items, create_recado_item,
    update_recado_item, delete_recado_item
)
from schemas.recado import RecadoItem, RecadoItemCreate, RecadoItemUpdate
from models.user import User

router = APIRouter(prefix="/recados", tags=["recados"])

@router.get("/", response_model=List[RecadoItem])
def read_recado_items(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filter by group: Coral, Orquestra, or Setor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    items = get_recado_items(db, skip=skip, limit=limit, group_filter=group_filter)
    return items

@router.post("/", response_model=RecadoItem)
def create_recado_item_endpoint(
    item: RecadoItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    return create_recado_item(db=db, item=item)

@router.get("/{item_id}", response_model=RecadoItem)
def read_recado_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_item = get_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado item not found")
    return db_item

@router.put("/{item_id}", response_model=RecadoItem)
def update_recado_item_endpoint(
    item_id: int,
    item_update: RecadoItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    db_item = update_recado_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado item not found")
    return db_item

@router.delete("/{item_id}")
def delete_recado_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    db_item = delete_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado item not found")
    return {"message": "Recado item deleted successfully"}
