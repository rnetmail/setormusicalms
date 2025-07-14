from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config_local import settings
from app.database_local import engine
from models import user, repertorio, agenda, recado
from app.routers import auth, users, repertorio as repertorio_router, agenda as agenda_router, recados

# Create database tables
user.Base.metadata.create_all(bind=engine)
repertorio.Base.metadata.create_all(bind=engine)
agenda.Base.metadata.create_all(bind=engine)
recado.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API - Local",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS (Ambiente Local)",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(repertorio_router.router, prefix="/api")
app.include_router(agenda_router.router, prefix="/api")
app.include_router(recados.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Setor Musical MS API is running (Local Environment)"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is running properly"}

