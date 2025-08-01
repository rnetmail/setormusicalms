# /fastapi_backend/app/routers/galeria.py
# v1.1 - 2025-07-30 02:17:05 - Corrige importações para o padrão absoluto do projeto.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session

# Correção: Importações absolutas a partir da raiz do pacote 'app'
from app import schemas
from app.database import get_db
from app.crud import galeria as crud_galeria
from app.crud import user as crud_user
# Assumindo que você terá um utilitário para lidar com uploads. Se não, esta linha pode ser removida.
# from app.utils import file_handler 

router = APIRouter()

@router.post("/", response_model=schemas.Galeria, status_code=status.HTTP_201_CREATED)
async def create_galeria_item(
    title: str,
    description: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria um novo item na galeria (imagem). Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Placeholder para a lógica de salvamento de arquivo.
    # Você precisará implementar a função 'save_upload_file' em algum lugar, como em 'app/utils/file_handler.py'.
    # file_url = await file_handler.save_upload_file(upload_file=file, destination="galeria")
    file_url = f"/static/images/galeria/{file.filename}" # Exemplo de URL
    
    item_schema = schemas.GaleriaCreate(title=title, description=description, image_url=file_url)
    
    return crud_galeria.create_galeria_item(db=db, item=item_schema)

@router.get("/", response_model=List[schemas.Galeria])
def read_galeria_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todos os itens da galeria.
    """
    items = crud_galeria.get_galeria_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=schemas.Galeria)
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
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
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
    # file_handler.delete_file(file_path=db_item.image_url)
        
    crud_galeria.delete_galeria_item(db=db, item_id=item_id)
    return {"ok": True}
