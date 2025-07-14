#!/usr/bin/env python3
"""
Script para criar usuário admin inicial (versão local SQLite)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database_local import SessionLocal, engine
from models.user import User
from auth.security import get_password_hash
from models import user, repertorio, agenda, recado

def create_tables():
    """Cria todas as tabelas no banco de dados"""
    user.Base.metadata.create_all(bind=engine)
    repertorio.Base.metadata.create_all(bind=engine)
    agenda.Base.metadata.create_all(bind=engine)
    recado.Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

def create_admin_user():
    """Cria ou atualiza o usuário admin"""
    db = SessionLocal()
    try:
        # Verifica se o admin já existe
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            # Atualiza o usuário existente
            admin_user.hashed_password = get_password_hash("Setor@MS25")
            admin_user.is_active = True
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.email = "admin@setormusicalms.art.br"
            print("✅ Usuário admin atualizado!")
        else:
            # Cria novo usuário admin
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
            print("✅ Usuário admin criado!")
        
        db.commit()
        print(f"Username: {admin_user.username}")
        print(f"Password: Setor@MS25")
        print(f"Email: {admin_user.email}")
        print(f"is_staff: {admin_user.is_staff}")
        print(f"is_superuser: {admin_user.is_superuser}")
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando banco de dados local...")
    create_tables()
    create_admin_user()
    print("✅ Inicialização concluída!")

