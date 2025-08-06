# /fastapi_backend/app/routers/galeria.py
# v2.0 - 2025-07-30 23:02:00 - Corrige importações para estrutura correta do projeto.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

# Importações corretas baseadas na estrutura real do projeto
from ...schemas import galeria as galeria_schemas, user as user_schemas
from ..database import get_db
from ...crud import galeria as crud_galeria, user as crud_user

router = APIRouter()

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
    
    # Placeholder para a lógica de salvamento de arquivo.
    # Você precisará implementar a função 'save_upload_file' em algum lugar, como em 'utils/file_handler.py'.
    file_url = f"/static/images/galeria/{file.filename}"  # Exemplo de URL
    
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
    
    # Lógica para deletar o arquivo físico, se necessário
    # file_handler.delete_file(file_path=db_item.imageUrl)
        
    crud_galeria.delete_galeria_item(db=db, item_id=item_id)
    return {"ok": True}

