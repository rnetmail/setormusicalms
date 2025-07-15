# setormusicalms/backend/init_simple.py
from database.database import SessionLocal, engine, Base
from models.user import User
from security.security import get_password_hash

def init_db():
    """
    Inicializa o banco de dados. Este é um script simplificado para criar
    as tabelas e um usuário administrador.
    """
    # Cria as tabelas baseadas nos modelos SQLAlchemy
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Verifica se o usuário 'admin' já existe
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # Cria o usuário se ele não existir
            hashed_password = get_password_hash("Setor@MS25")
            admin_user = User(
                username="admin", 
                hashed_password=hashed_password, 
                is_superuser=True, 
                is_staff=True,
                active=True
            )
            db.add(admin_user)
            db.commit()
            print("Usuário 'admin' criado com sucesso.")
            print(f"Username: {admin_user.username}")
            # Corrigido: Removido o f-string desnecessário
            print("Password: Setor@MS25")
            print(f"is_staff: {admin_user.is_staff}")
            print(f"is_superuser: {admin_user.is_superuser}")
        else:
            print("Usuário 'admin' já existe.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
