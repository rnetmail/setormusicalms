#!/usr/bin/env python
"""
Script para inicializar o banco de dados com dados básicos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import RepertorioItem, AgendaItem, RecadoItem, HistoriaItem, GaleriaItem

def create_superuser():
    """Criar superusuário se não existir"""
    username = os.environ.get('ADMIN_USER', 'admin')
    password = os.environ.get('ADMIN_PASS', 'Setor@MS25')
    email = 'admin@setormusicalms.art.br'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superusuário '{username}' criado com sucesso!")
    else:
        print(f"ℹ️ Superusuário '{username}' já existe.")

def create_sample_data():
    """Criar dados de exemplo se não existirem"""
    
    # Verificar se já existem dados
    if RepertorioItem.objects.exists():
        print("ℹ️ Dados de exemplo já existem.")
        return
    
    print("📝 Criando dados de exemplo...")
    
    # Repertório de exemplo
    RepertorioItem.objects.create(
        type='Coral',
        title='Ave Maria',
        arrangement='Franz Schubert',
        year=2024,
        audioUrl='https://drive.google.com/uc?export=download&id=EXEMPLO_AUDIO',
        videoUrl='https://www.youtube.com/watch?v=EXEMPLO_VIDEO',
        sheetMusicUrl='https://drive.google.com/file/d/EXEMPLO_PDF/preview',
        naipes=['Soprano', 'Contralto', 'Tenor', 'Baixo'],
        active=True
    )
    
    RepertorioItem.objects.create(
        type='Orquestra',
        title='Estudo em Mi Maior',
        arrangement='Fernando Sor',
        year=2024,
        audioUrl='https://drive.google.com/uc?export=download&id=EXEMPLO_AUDIO2',
        sheetMusicUrl='https://drive.google.com/file/d/EXEMPLO_PDF2/preview',
        grupos=['Grupo 1', 'Grupo 2'],
        active=True
    )
    
    # Agenda de exemplo
    from datetime import date, timedelta
    
    AgendaItem.objects.create(
        group='Coral',
        date=date.today() + timedelta(days=7),
        title='Ensaio Geral',
        description='Ensaio geral para apresentação do próximo domingo.',
        active=True
    )
    
    AgendaItem.objects.create(
        group='Orquestra',
        date=date.today() + timedelta(days=14),
        title='Apresentação Especial',
        description='Apresentação especial na igreja matriz.',
        active=True
    )
    
    # Recados de exemplo
    RecadoItem.objects.create(
        group='Setor',
        date=date.today(),
        title='Bem-vindos ao Sistema',
        description='Sistema de gestão do Setor Musical está funcionando!',
        active=True
    )
    
    # História de exemplo
    HistoriaItem.objects.create(
        year=2024,
        title='Lançamento do Sistema Digital',
        description='Implementação do sistema digital para gestão do repertório e atividades.',
        imageUrl='https://via.placeholder.com/400x300?text=Sistema+Digital'
    )
    
    print("✅ Dados de exemplo criados com sucesso!")

def main():
    """Função principal"""
    print("🚀 Inicializando banco de dados...")
    
    try:
        create_superuser()
        create_sample_data()
        print("🎉 Inicialização concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante inicialização: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

