#!/usr/bin/env python
"""
Script para criar usuário administrador
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Cria usuário administrador se não existir"""
    
    # Dados do admin
    username = 'admin'
    email = 'admin@setormusicalms.art.br'
    password = 'Setor@MS25'
    
    # Verificar se já existe
    if User.objects.filter(username=username).exists():
        print(f"✅ Usuário '{username}' já existe")
        user = User.objects.get(username=username)
    else:
        # Criar usuário
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Usuário administrador '{username}' criado com sucesso!")
    
    # Garantir que é superuser e staff
    user.is_superuser = True
    user.is_staff = True
    user.save()
    
    print(f"📋 Dados do usuário:")
    print(f"   Username: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Is Staff: {user.is_staff}")
    print(f"   Is Superuser: {user.is_superuser}")
    print(f"   Password: {password}")
    
    return user

if __name__ == '__main__':
    try:
        create_admin_user()
        print("🎉 Script executado com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

