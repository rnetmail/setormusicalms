# setormusicalms\backend\init_admin.py

from database.database import SessionLocal, engine, Base
from models.user import User
from security.security import get_password_hash

# Senha padrão para o usuário admin
ADMIN_PASSWORD = "Setor@MS25"

        db.add(admin_user)
        db.commit()
        print(f"Username: {admin_user.username}")
        print("Password: Setor@MS25")
        print(f"is_staff: {admin_user.is_staff}")
        print(f"is_superuser: {admin_user.is_superuser}")
    else:
