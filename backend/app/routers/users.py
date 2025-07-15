#setormusicalms/backend/app/routers/users.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from auth.security import get_current_superuser
from crud.user import (
    get_user, get_users, create_user, update_user, delete_user,
)

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from models.repertorio import RepertorioItem
from schemas.repertorio import RepertorioItemCreate, RepertorioItemUpdate


    # Filtrar apenas ativos
    if active_only:
        query = query.filter(RepertorioItem.active)
    
    # Ordenar por ano e título
    query = query.order_by(RepertorioItem.year.desc(), RepertorioItem.title)
    return db.query(RepertorioItem).filter(
        and_(
            RepertorioItem.type == group_type,
            RepertorioItem.active
        )
    ).order_by(RepertorioItem.year.desc(), RepertorioItem.title).all()


from models.user import User
from schemas.user import UserCreate, UserUpdate
from auth.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
