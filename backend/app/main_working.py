from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import re

# Configuração do banco SQLite
DATABASE_URL = "sqlite:///./setor_musical.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuração de autenticação
SECRET_KEY = "sua-chave-secreta-super-forte-aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos SQLAlchemy
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class RepertorioItem(Base):
    __tablename__ = "repertorio_items"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # Coral, Orquestra, Setor
    title = Column(String, nullable=False)
    arrangement = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    sheet_music_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    naipes = Column(JSON, nullable=True)
    grupos = Column(JSON, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class AgendaItem(Base):
    __tablename__ = "agenda_items"
    
    id = Column(Integer, primary_key=True, index=True)
    group = Column(String, nullable=False)  # Coral, Orquestra, Setor
    date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class RecadoItem(Base):
    __tablename__ = "recado_items"
    
    id = Column(Integer, primary_key=True, index=True)
    group = Column(String, nullable=False)  # Coral, Orquestra, Setor
    date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

# Schemas Pydantic
class UserBase(BaseModel):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RepertorioBase(BaseModel):
    type: str
    title: str
    arrangement: Optional[str] = None
    year: Optional[int] = None
    sheet_music_url: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    naipes: Optional[List[str]] = None
    grupos: Optional[List[str]] = None
    active: bool = True

class RepertorioCreate(RepertorioBase):
    pass

class RepertorioResponse(RepertorioBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AgendaBase(BaseModel):
    group: str
    date: str
    title: str
    description: Optional[str] = None
    active: bool = True

class AgendaCreate(AgendaBase):
    pass

class AgendaResponse(AgendaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class RecadoBase(BaseModel):
    group: str
    date: str
    title: str
    description: Optional[str] = None
    active: bool = True

class RecadoCreate(RecadoBase):
    pass

class RecadoResponse(RecadoBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Funções de conversão de mídia
def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    if not url or "drive.google.com" not in url:
        return url
    
    file_id_match = re.search(r'/file/d/([a-zA-Z0-9-_]+)', url)
    if not file_id_match:
        return url
    
    file_id = file_id_match.group(1)
    
    if media_type == "audio":
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    elif media_type == "pdf":
        return f"https://drive.google.com/file/d/{file_id}/preview"
    else:
        return f"https://drive.google.com/file/d/{file_id}/preview"

def convert_youtube_link(url: str) -> str:
    if not url or "youtu" not in url:
        return url
    
    video_id = None
    if "youtu.be/" in url:
        video_id_match = re.search(r'youtu\.be/([a-zA-Z0-9-_]+)', url)
        if video_id_match:
            video_id = video_id_match.group(1)
    elif "youtube.com/watch" in url:
        video_id_match = re.search(r'[?&]v=([a-zA-Z0-9-_]+)', url)
        if video_id_match:
            video_id = video_id_match.group(1)
    
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return url

def process_media_urls(data: dict) -> dict:
    processed = data.copy()
    
    if "audio_url" in processed and processed["audio_url"]:
        if "drive.google.com" in processed["audio_url"]:
            processed["audio_url"] = convert_google_drive_link(processed["audio_url"], "audio")
    
    if "video_url" in processed and processed["video_url"]:
        if "youtu" in processed["video_url"]:
            processed["video_url"] = convert_youtube_link(processed["video_url"])
        elif "drive.google.com" in processed["video_url"]:
            processed["video_url"] = convert_google_drive_link(processed["video_url"], "video")
    
    if "sheet_music_url" in processed and processed["sheet_music_url"]:
        if "drive.google.com" in processed["sheet_music_url"]:
            processed["sheet_music_url"] = convert_google_drive_link(processed["sheet_music_url"], "pdf")
    
    return processed

# Funções de autenticação
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Criar aplicação FastAPI
app = FastAPI(
    title="Setor Musical MS API - Funcional",
    description="API funcional para gerenciamento do Setor Musical",
    version="1.0.2"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar usuário admin se não existir
def create_admin_user():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@setormusicalms.art.br",
                hashed_password=get_password_hash("Setor@MS25"),
                first_name="Admin",
                last_name="Sistema",
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuário admin criado!")
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
    finally:
        db.close()

create_admin_user()

# Rotas
@app.get("/")
def read_root():
    return {
        "message": "Setor Musical MS API - Funcional",
        "version": "1.0.2",
        "status": "running"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API funcionando corretamente",
        "features": ["filtros_por_grupo", "conversao_midia", "cors_habilitado"]
    }

@app.post("/api/auth/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas de Repertório
@app.get("/api/repertorio/", response_model=List[RepertorioResponse])
def list_repertorio(
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(RepertorioItem).filter(RepertorioItem.active == True)
    if type_filter:
        query = query.filter(RepertorioItem.type == type_filter)
    return query.offset(skip).limit(limit).all()

@app.get("/api/repertorio/by-group/{group_type}", response_model=List[RepertorioResponse])
def list_repertorio_by_group(
    group_type: str,
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    if group_type not in ["Coral", "Orquestra", "Setor"]:
        raise HTTPException(status_code=400, detail="Grupo deve ser: Coral, Orquestra ou Setor")
    
    query = db.query(RepertorioItem).filter(
        RepertorioItem.type == group_type,
        RepertorioItem.active == True
    )
    if year:
        query = query.filter(RepertorioItem.year == year)
    
    return query.order_by(RepertorioItem.title).all()

@app.post("/api/repertorio/", response_model=RepertorioResponse)
def create_repertorio(item: RepertorioCreate, db: Session = Depends(get_db)):
    # Processar URLs de mídia
    item_data = item.dict()
    processed_data = process_media_urls(item_data)
    
    db_item = RepertorioItem(**processed_data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Rotas de Agenda
@app.get("/api/agenda/", response_model=List[AgendaResponse])
def list_agenda(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AgendaItem).filter(AgendaItem.active == True)
    if group_filter:
        query = query.filter(AgendaItem.group == group_filter)
    return query.offset(skip).limit(limit).all()

@app.get("/api/agenda/by-group/{group_type}", response_model=List[AgendaResponse])
def list_agenda_by_group(group_type: str, db: Session = Depends(get_db)):
    if group_type not in ["Coral", "Orquestra", "Setor"]:
        raise HTTPException(status_code=400, detail="Grupo deve ser: Coral, Orquestra ou Setor")
    
    return db.query(AgendaItem).filter(
        AgendaItem.group == group_type,
        AgendaItem.active == True
    ).order_by(AgendaItem.date.desc()).all()

@app.post("/api/agenda/", response_model=AgendaResponse)
def create_agenda(item: AgendaCreate, db: Session = Depends(get_db)):
    db_item = AgendaItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Rotas de Recados
@app.get("/api/recados/", response_model=List[RecadoResponse])
def list_recados(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(RecadoItem).filter(RecadoItem.active == True)
    if group_filter:
        query = query.filter(RecadoItem.group == group_filter)
    return query.offset(skip).limit(limit).all()

@app.get("/api/recados/by-group/{group_type}", response_model=List[RecadoResponse])
def list_recados_by_group(group_type: str, db: Session = Depends(get_db)):
    if group_type not in ["Coral", "Orquestra", "Setor"]:
        raise HTTPException(status_code=400, detail="Grupo deve ser: Coral, Orquestra ou Setor")
    
    return db.query(RecadoItem).filter(
        RecadoItem.group == group_type,
        RecadoItem.active == True
    ).order_by(RecadoItem.date.desc()).all()

@app.post("/api/recados/", response_model=RecadoResponse)
def create_recado(item: RecadoCreate, db: Session = Depends(get_db)):
    db_item = RecadoItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

