# backend/app/config.py

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
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

        db.add(admin_user)
        db.commit()
        print(f"Username: {admin_user.username}")
        print("Password: Setor@MS25")
        print(f"is_staff: {admin_user.is_staff}")
        print(f"is_superuser: {admin_user.is_superuser}")
    else:
from pydantic import BaseModel
from typing import Optional, List

class RepertorioItemBase(BaseModel):
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        time.sleep(2)
    except Exception:
        pass

def start_fastapi_server():
            if "Uvicorn running on" in line:
                print("✅ Servidor FastAPI iniciado com sucesso!")
                return process
        except Exception:
            time.sleep(1)
    stop_fastapi_server(process)
    raise RuntimeError("❌ Não foi possível iniciar o servidor FastAPI a tempo.")


