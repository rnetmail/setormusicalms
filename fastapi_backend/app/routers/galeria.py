# /fastapi_backend/app/routers/galeria.py
# v2.1 - 2025-08-07 - Corrige importações para absolutas.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

# --- INÍCIO DA CORREÇÃO ---
from app.schemas import galeria as galeria_schemas, user as user_schemas
from app.database import get_db
from app.crud import galeria as crud_galeria, user as crud_user
# --- FIM DA CORREÇÃO ---

router = APIRouter(prefix="/api/galeria", tags=["Galeria"])

@router.post("/", response_model=galeria_schemas.GaleriaItem, status_code=status.HTTP_201_CREATED)
async def create_galeria_item(
    title: str,
    description: str,
    group: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria um novo item na galeria (imagem). Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    file_url = f"/static/images/galeria/{file.filename}"
    
    from datetime import date
    item_schema = galeria_schemas.GaleriaItemCreate(
        title=title, 
        description=description, 
        group=group,
        imageUrl=file_url,
        date=date.today()
    )
    
    return crud_galeria.create_galeria_item(db=db, item=item_schema)

@router.get("/", response_model=List[galeria_schemas.GaleriaItem])
def read_galeria_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todos os itens da galeria.
    """
    items = crud_galeria.get_galeria_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=galeria_schemas.GaleriaItem)
def read_galeria_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retorna um item específico da galeria pelo ID.
    """
    db_item = crud_galeria.get_galeria_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Galeria item not found")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_galeria_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Deleta um item da galeria. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    db_item = crud_galeria.get_galeria_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Galeria item not found")
        
    crud_galeria.delete_galeria_item(db=db, item_id=item_id)
    return {"ok": True}
