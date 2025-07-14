from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user
from crud.agenda import (
    get_agenda_item, get_agenda_items, create_agenda_item,
    update_agenda_item, delete_agenda_item
)
from schemas.agenda import AgendaItem, AgendaItemCreate, AgendaItemUpdate
from models.user import User

router = APIRouter(prefix="/agenda", tags=["agenda"])

@router.get("/", response_model=List[AgendaItem])
def read_agenda_items(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filter by group: Coral, Orquestra, or Setor"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    items = get_agenda_items(db, skip=skip, limit=limit, group_filter=group_filter)
    return items

@router.post("/", response_model=AgendaItem)
def create_agenda_item_endpoint(
    item: AgendaItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    return create_agenda_item(db=db, item=item)

@router.get("/{item_id}", response_model=AgendaItem)
def read_agenda_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_item = get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Agenda item not found")
    return db_item

@router.put("/{item_id}", response_model=AgendaItem)
def update_agenda_item_endpoint(
    item_id: int,
    item_update: AgendaItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    db_item = update_agenda_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Agenda item not found")
    return db_item

@router.delete("/{item_id}")
def delete_agenda_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff_user)
):
    db_item = delete_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Agenda item not found")
    return {"message": "Agenda item deleted successfully"}
