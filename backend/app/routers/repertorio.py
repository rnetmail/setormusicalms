from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user
from crud.repertorio import (
    get_repertorio_item, get_repertorio_items, create_repertorio_item,
    update_repertorio_item, delete_repertorio_item
)
from schemas.repertorio import RepertorioItem, RepertorioItemCreate, RepertorioItemUpdate
from models.user import User

router = APIRouter(prefix="/repertorio", tags=["repertorio"])

@router.get("/", response_model=List[RepertorioItem])
def read_repertorio_items(
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None, description="Filter by type: Coral, Orquestra, or Setor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    items = get_repertorio_items(db, skip=skip, limit=limit, type_filter=type_filter)
    return items

@router.post("/", response_model=RepertorioItem)
def create_repertorio_item_endpoint(
    item: RepertorioItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    return create_repertorio_item(db=db, item=item)

@router.get("/{item_id}", response_model=RepertorioItem)
def read_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_item = get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Repertorio item not found")
    return db_item

@router.put("/{item_id}", response_model=RepertorioItem)
def update_repertorio_item_endpoint(
    item_id: int,
    item_update: RepertorioItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    db_item = update_repertorio_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Repertorio item not found")
    return db_item

@router.delete("/{item_id}")
def delete_repertorio_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    db_item = delete_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Repertorio item not found")
    return {"message": "Repertorio item deleted successfully"}

