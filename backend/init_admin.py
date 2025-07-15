# setormusicalms/backend/init_admin.py
from database.database import SessionLocal, engine, Base
from models.user import User
from security.security import get_password_hash

# É melhor gerenciar segredos via variáveis de ambiente, mas para simplicidade,
# definimos a senha padrão aqui.
ADMIN_PASSWORD = "Setor@MS25"

def init_db():
    """
    Inicializa o banco de dados. Cria todas as tabelas e um superusuário padrão
    se ele ainda não existir.
    """
    # Este comando cria as tabelas do banco de dados com base nos seus modelos.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Verifica se o usuário 'admin' já existe para evitar duplicatas.
        admin_user = db.query(User).filter(User.username == "admin").first()

        if not admin_user:
            # Se o usuário não existir, cria um novo.
            hashed_password = get_password_hash(ADMIN_PASSWORD)
            new_admin = User(
                username="admin",
                hashed_password=hashed_password,
                is_superuser=True,
                is_staff=True,
                active=True
            )
            db.add(new_admin)
            db.commit()
            print(">>> Usuário 'admin' criado com sucesso.")
            print(f">>> Senha: {ADMIN_PASSWORD}")
        else:
            print(">>> Usuário 'admin' já existe. Nenhuma ação foi necessária.")

    finally:
        # É crucial fechar a sessão do banco de dados para liberar recursos.
        db.close()

if __name__ == "__main__":
    print("Iniciando a criação do usuário administrador padrão...")
    init_db()
    print("Processo finalizado.")
