# fastapi_backend/init_admin.py
# Versão 25 18/07/2025 00:21
from app.database import SessionLocal, engine, Base
from models.user import User
# CORREÇÃO: Importa a função do novo ficheiro 'auth/password.py'.
from auth.password import get_password_hash

# Importa todos os modelos para garantir que o SQLAlchemy os reconheça ao criar as tabelas.
from models import repertorio, agenda, recado

def create_database_and_tables():
    """Cria o ficheiro do banco de dados e todas as tabelas, se não existirem."""
    print("A criar tabelas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

def create_admin_user():
    """Cria o usuário 'admin' com permissões de superusuário se ele não existir."""
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
            print(f"Usuário '{admin_username}' já existe, nenhuma ação necessária.")
        
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
