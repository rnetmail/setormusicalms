# setormusicalms\backend\init_admin.py

from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from database.database import SessionLocal, engine, Base
from models.user import User
from security.security import get_password_hash
import os

# Senha padrão para o usuário admin
ADMIN_PASSWORD = "Setor@MS25"

def initialize_database():
    print("🚀 Inicializando banco de dados...")
    
    # Garante que todas as tabelas sejam criadas
    print("🔧 Verificando e criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas prontas.")

    db = SessionLocal()
    try:
        # Verifica se o usuário admin já existe
        admin_user = db.query(User).filter(User.username == "admin").first()
        hashed_password = get_password_hash(ADMIN_PASSWORD)

        if not admin_user:
            print("🔧 Criando usuário admin...")
            hashed_password = get_password_hash("Setor@MS25")
            print("➕ Criando usuário 'admin'...")
            db_user = User(username="admin", hashed_password=hashed_password, is_active=True)
            db.add(db_user)
            print("✅ Usuário admin criado!")
            print("✅ Usuário 'admin' criado com sucesso!")
        else:
            print("ℹ️ Usuário admin já existe.")
            print("🔄 Atualizando senha do usuário 'admin'...")
            admin_user.hashed_password = hashed_password
            print("✅ Senha do usuário 'admin' atualizada com sucesso!")
        
        db.commit()

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a inicialização: {e}")
        db.rollback()
    finally:
        db.close()
    print("✅ Inicialização concluída!")
        
    print("✅ Inicialização do banco de dados concluída!")

if __name__ == "__main__":
    initialize_database()