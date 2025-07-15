# setormusicalms\backend\init_admin.py

# Senha padrão para o usuário admin
ADMIN_PASSWORD = "Setor@MS25"

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        admin_user = User(username="admin", hashed_password=hashed_password, is_superuser=True, is_staff=True, active=True)
        db.add(admin_user)
        db.commit()
        print(f"Admin user created: Username: {admin_user.username}, Password: {ADMIN_PASSWORD}")
    else:
        print(f"Admin user '{admin_user.username}' already exists.")
    db.close()

if __name__ == "__main__":
    init_db()
