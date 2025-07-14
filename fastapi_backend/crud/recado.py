from sqlalchemy.orm import Session
from models.recado import RecadoItem
from schemas.recado import RecadoItemCreate, RecadoItemUpdate

def get_recado_item(db: Session, item_id: int):
    return db.query(RecadoItem).filter(RecadoItem.id == item_id).first()

def get_recado_items(db: Session, skip: int = 0, limit: int = 100, group_filter: str = None):
    query = db.query(RecadoItem)
    if group_filter:
        query = query.filter(RecadoItem.group == group_filter)
    return query.order_by(RecadoItem.date.desc()).offset(skip).limit(limit).all()

def create_recado_item(db: Session, item: RecadoItemCreate):
    db_item = RecadoItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_recado_item(db: Session, item_id: int, item_update: RecadoItemUpdate):
    db_item = db.query(RecadoItem).filter(RecadoItem.id == item_id).first()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_recado_item(db: Session, item_id: int):
    db_item = db.query(RecadoItem).filter(RecadoItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
