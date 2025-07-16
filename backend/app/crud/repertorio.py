from sqlalchemy.orm import Session
from models.repertorio import RepertorioItem
from schemas.repertorio import RepertorioItemCreate, RepertorioItemUpdate

def get_repertorio_item(db: Session, item_id: int):
    return db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()

def get_repertorio_items(db: Session, skip: int = 0, limit: int = 100, type_filter: str = None):
    query = db.query(RepertorioItem)
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)
    return query.order_by(RepertorioItem.year.desc(), RepertorioItem.title).offset(skip).limit(limit).all()

def create_repertorio_item(db: Session, item: RepertorioItemCreate):
    db_item = RepertorioItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_repertorio_item(db: Session, item_id: int, item_update: RepertorioItemUpdate):
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_repertorio_item(db: Session, item_id: int):
    db_item = db.query(RepertorioItem).filter(RepertorioItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

