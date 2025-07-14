from sqlalchemy.orm import Session
from models.agenda import AgendaItem
from schemas.agenda import AgendaItemCreate, AgendaItemUpdate

def get_agenda_item(db: Session, item_id: int):
    return db.query(AgendaItem).filter(AgendaItem.id == item_id).first()

def get_agenda_items(db: Session, skip: int = 0, limit: int = 100, group_filter: str = None):
    query = db.query(AgendaItem)
    if group_filter:
        query = query.filter(AgendaItem.group == group_filter)
    return query.order_by(AgendaItem.date.desc()).offset(skip).limit(limit).all()

def create_agenda_item(db: Session, item: AgendaItemCreate):
    db_item = AgendaItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_agenda_item(db: Session, item_id: int, item_update: AgendaItemUpdate):
    db_item = db.query(AgendaItem).filter(AgendaItem.id == item_id).first()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_agenda_item(db: Session, item_id: int):
    db_item = db.query(AgendaItem).filter(AgendaItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
