# fastapi_backend/init_admin.py
# Versão 48 17/07/2025 23:40
import sys
import os

# Adiciona o diretório raiz ao path para garantir que as importações funcionem
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# A importação da 'app' está correta pois refere-se à pasta /app/app
from app.database import SessionLocal, engine, Base
# CORREÇÃO: Os modelos estão na pasta 'models', não 'app/models'
from models.user import User
from auth.security import get_password_hash
# CORREÇÃO: Importa os outros modelos do caminho correto
from models import repertorio, agenda, recado

def create_database_and_tables():
    """Cria o ficheiro .db e todas as tabelas no banco de dados se não existirem."""
    print("A criar tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

def create_admin_user():
    """Cria ou atualiza o usuário 'admin' com permissões de superusuário."""
    db = SessionLocal()
    try:
        admin_username = "admin"
        admin_password = "Setor@MS25"
        
        admin_user = db.query(User).filter(User.username == admin_username).first()
        
        if not admin_user:
            print(f"A criar o usuário '{admin_username}'...")
            admin_user = User(
                username=admin_username,
                email="admin@setormusicalms.art.br",
                hashed_password=get_password_hash(admin_password),
                first_name="Admin",
                last_name="Sistema",
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuário admin criado!")
        else:
            print(f"Usuário '{admin_username}' já existe.")
        
    except Exception as e:
        print(f"❌ Erro ao criar/verificar o usuário admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 A iniciar a inicialização do banco de dados...")
    create_database_and_tables()
    create_admin_user()
    print("✅ Processo de inicialização concluído!")
