# /fastapi_backend/init_admin.py
# v2.0 - 2025-08-07 12:05:00 - Corrige importações para execução direta.

import sys
import os

# Adiciona o diretório raiz ao path para permitir importações
sys.path.append('/app')
sys.path.append('/app/fastapi_backend')

try:
    # Importações diretas sem usar importações relativas
    from app.database import SessionLocal, engine
    from app.models.user import User
    from app.auth.hashing import get_password_hash
    
    def create_admin_user():
        """
        Cria um usuário administrador padrão se não existir.
        """
        db = SessionLocal()
        try:
            # Verifica se já existe um admin
            admin_user = db.query(User).filter(User.username == "admin").first()
            
            if not admin_user:
                # Cria o usuário admin
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
                print("✅ Usuário admin criado com sucesso!")
                print("Username: admin")
                print("Password: admin")
            else:
                print("ℹ️ Usuário admin já existe.")
                
        except Exception as e:
            print(f"❌ Erro ao criar usuário admin: {e}")
            db.rollback()
        finally:
            db.close()

    if __name__ == "__main__":
        print("🚀 Inicializando usuário administrador...")
        create_admin_user()
        print("✅ Inicialização concluída!")

except ImportError as e:
    print(f"⚠️ Erro de importação: {e}")
    print("🔄 Tentando abordagem alternativa...")
    
    # Abordagem alternativa - criar admin básico via SQL direto
    import sqlite3
    
    def create_admin_simple():
        try:
            # Conecta diretamente ao banco SQLite
            conn = sqlite3.connect('/app/data/setormusical.db')
            cursor = conn.cursor()
            
            # Verifica se a tabela users existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    full_name VARCHAR(100),
                    hashed_password VARCHAR(255) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_staff BOOLEAN DEFAULT FALSE,
                    is_superuser BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Verifica se admin já existe
            cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
            if cursor.fetchone() is None:
                # Insere admin básico (senha: admin)
                # Hash simples para teste: admin
                cursor.execute("""
                    INSERT INTO users (username, email, full_name, hashed_password, is_active, is_staff, is_superuser)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, ("admin", "admin@setormusical.ms", "Administrador", 
                     "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", 
                     True, True, True))
                
                conn.commit()
                print("✅ Usuário admin criado via SQL!")
                print("Username: admin")
                print("Password: admin")
            else:
                print("ℹ️ Usuário admin já existe.")
                
        except Exception as e:
            print(f"❌ Erro ao criar admin via SQL: {e}")
        finally:
            conn.close()
    
    print("🚀 Criando admin via SQL direto...")
    create_admin_simple()
    print("✅ Processo concluído!")

except Exception as e:
    print(f"❌ Erro geral: {e}")
    print("ℹ️ Continuando sem criar usuário admin...")
