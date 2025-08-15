# /fastapi_backend/init_admin.py
# v4.0 - 2025-08-10 20:30 - Fix ImportError - Remove app folder references

# Importa os módulos necessários diretamente, pois estão na mesma raiz.
from database import SessionLocal
from models.user import User
from auth.security import get_password_hash

def create_admin_user():
        """
            Cria um usuário administrador padrão ('admin') se ele não existir.
                """
        # Cria uma nova sessão com o banco de dados.
        db = SessionLocal()

    try:
                # Verifica se o usuário 'admin' já existe no banco.
                admin_user = db.query(User).filter(User.username == "admin").first()

        if not admin_user:
                        # Se não existir, cria um novo usuário administrador.
                        # A senha "admin" é transformada em um hash seguro.
                        hashed_password = get_password_hash("admin")

            admin_user = User(
                                username="admin",
                                email="admin@setormusical.ms",
                                full_name="Administrador",
                                hashed_password=hashed_password,
                                is_active=True,
                                is_staff=True,
                                is_superuser=True
            )

            db.add(admin_user)
            db.commit()
            print("✅ Usuário 'admin' criado com sucesso!")
            print("   - Username: admin")
            print("   - Password: admin (use esta senha para o primeiro login)")
else:
            print("ℹ️ Usuário 'admin' já existe. Nenhuma ação necessária.")

except Exception as e:
            print(f"❌ Erro ao tentar criar o usuário administrador: {e}")
            db.rollback()
finally:
            # Garante que a sessão com o banco de dados seja sempre fechada.
            db.close()

if __name__ == "__main__":
        print("🚀 Executando script de inicialização do administrador...")
        create_admin_user()
        print("✅ Script de inicialização concluído.")
