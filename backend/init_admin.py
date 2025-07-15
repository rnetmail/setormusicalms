# setormusicalms\backend\init_admin.py
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.user import User
from security.security import get_password_hash
import os

def initialize_database():
    print("🚀 Inicializando banco de dados...")
    db = SessionLocal()
    try:
        # Verifica se o usuário admin já existe
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("🔧 Criando usuário admin...")
            hashed_password = get_password_hash("Setor@MS25")
            db_user = User(username="admin", hashed_password=hashed_password, is_active=True)
            db.add(db_user)
            db.commit()
            print("✅ Usuário admin criado!")
        else:
            print("ℹ️ Usuário admin já existe.")
    finally:
        db.close()
    print("✅ Inicialização concluída!")

if __name__ == "__main__":
    initialize_database()