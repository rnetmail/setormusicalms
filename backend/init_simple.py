#!/usr/bin/env python3
"""
Script simplificado para criar usuário admin
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from passlib.context import CryptContext

# Configuração do banco SQLite
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo User simplificado
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

# Configuração de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def main():
    print("🚀 Criando banco de dados e usuário admin...")
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas!")
    
    # Criar usuário admin
    db = SessionLocal()
    try:
        # Verificar se admin já existe
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if admin_user:
            # Atualizar senha
            admin_user.hashed_password = get_password_hash("Setor@MS25")
            admin_user.is_active = True
            admin_user.is_staff = True
            admin_user.is_superuser = True
            print("✅ Usuário admin atualizado!")
        else:
            # Criar novo admin
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
        print(f"is_staff: {admin_user.is_staff}")
        print(f"is_superuser: {admin_user.is_superuser}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("✅ Inicialização concluída!")

if __name__ == "__main__":
    main()

