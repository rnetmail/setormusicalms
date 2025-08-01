# fastapi_backend/init_admin.py
# Versão 04 - FINAL

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from crud import user as crud_user
from schemas import user as schema_user

def init_db():
    # Cria as tabelas no banco de dados
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Verifica se o usuário 'admin' já existe
        admin_user = crud_user.get_user_by_username(db, username="admin")
        if not admin_user:
            print("Criando usuário administrador padrão...")
            user_in = schema_user.UserCreate(
                username="admin",
                password="Setor@MS25",
                email="admin@setormusicalms.art.br",
                full_name="Administrador do Sistema",
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            # Agora a função create_user existe e será chamada corretamente
            crud_user.create_user(db=db, user=user_in)
            print("Usuário administrador criado com sucesso.")
        else:
            print("Usuário administrador já existe.")
    finally:
        db.close()

if __name__ == "__main__":
    print("Inicializando o banco de dados...")
    init_db()
