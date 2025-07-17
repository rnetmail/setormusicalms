# fastapi_backend/init_admin.py
# Versão 31 17/07/2025 22:30
import sys
import os

# Adiciona o diretório raiz ao path para permitir importações relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from auth.security import get_password_hash
# Importar todos os modelos para garantir que todas as tabelas sejam criadas
from app.models import repertorio, agenda, recado

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
        admin_password = "Setor@MS25"  # Recomenda-se usar uma variável de ambiente para isso
        
        # Verifica se o usuário admin já existe
        admin_user = db.query(User).filter(User.username == admin_username).first()
        
        if admin_user:
            print(f"Usuário '{admin_username}' já existe. A verificar a senha...")
            # Opcional: pode-se atualizar a senha se necessário
            # admin_user.hashed_password = get_password_hash(admin_password)
        else:
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
            print("✅ Usuário admin criado!")
        
        db.commit()
        
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
