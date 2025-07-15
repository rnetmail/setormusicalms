#!/usr/bin/env python3
"""
Script completo para testar FastAPI com filtros por grupo
"""
import sys
import os
import subprocess
import time
import requests
import json
from datetime import datetime, date

# Adicionar path do FastAPI
sys.path.append('/home/ubuntu/setormusicalms/fastapi_backend')

def start_fastapi_server():
    """Inicia o servidor FastAPI"""
    print("🚀 Iniciando servidor FastAPI...")
    
    # Matar processos uvicorn existentes
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        time.sleep(2)
    except:
        pass
    
    # Iniciar novo servidor
    cmd = [
        "uvicorn", 
        "app.main_fixed:app", 
        "--host", "0.0.0.0", 
        "--port", "8001", 
        "--reload"
    ]
    
    env = os.environ.copy()
    env["PATH"] = env.get("PATH", "") + ":/home/ubuntu/.local/bin"
    
    process = subprocess.Popen(
        cmd,
        cwd="/home/ubuntu/setormusicalms/fastapi_backend",
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aguardar servidor iniciar
    for i in range(10):
        try:
            response = requests.get("http://localhost:8001/", timeout=2)
            if response.status_code == 200:
                print("✅ Servidor FastAPI iniciado com sucesso!")
                return process
        except:
            time.sleep(1)
    
    print("❌ Falha ao iniciar servidor FastAPI")
    return None

def test_health_check():
    """Testa endpoint de health"""
    try:
        response = requests.get("http://localhost:8001/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data}")
            return True
        else:
            print(f"❌ Health Check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}")
        return False

def test_login():
    """Testa login e retorna token"""
    try:
        login_data = {
            "username": "admin",
            "password": "Setor@MS25"
        }
        response = requests.post("http://localhost:8001/api/auth/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Login realizado: {token[:20]}...")
            return token
        else:
            print(f"❌ Login falhou: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None

def test_repertorio_filters(token):
    """Testa filtros de repertório por grupo"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n📋 TESTANDO FILTROS DE REPERTÓRIO")
    
    # Teste 1: Listar todos
    try:
        response = requests.get("http://localhost:8001/api/repertorio/", headers=headers, timeout=10)
        if response.status_code == 200:
            items = response.json()
            print(f"✅ Total de itens: {len(items)}")
        else:
            print(f"❌ Erro ao listar todos: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 2: Filtrar por Coral
    try:
        response = requests.get("http://localhost:8001/api/repertorio/by-group/Coral", headers=headers, timeout=10)
        if response.status_code == 200:
            coral_items = response.json()
            print(f"✅ Itens do Coral: {len(coral_items)}")
        else:
            print(f"❌ Erro ao filtrar Coral: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 3: Filtrar por Orquestra
    try:
        response = requests.get("http://localhost:8001/api/repertorio/by-group/Orquestra", headers=headers, timeout=10)
        if response.status_code == 200:
            orquestra_items = response.json()
            print(f"✅ Itens da Orquestra: {len(orquestra_items)}")
        else:
            print(f"❌ Erro ao filtrar Orquestra: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 4: Criar item para Coral
    try:
        new_item = {
            "type": "Coral",
            "title": "Teste Coral - Ave Maria",
            "arrangement": "Arranjo Teste",
            "year": 2024,
            "sheet_music_url": "https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/view",
            "audio_url": "https://drive.google.com/file/d/1XRwHe9d8jJRqU3DxR49b4dkVID__douV/view",
            "naipes": ["Soprano", "Contralto"],
            "grupos": ["Grupo 1"],
            "active": True
        }
        response = requests.post("http://localhost:8001/api/repertorio/", json=new_item, headers=headers, timeout=10)
        if response.status_code == 200:
            created_item = response.json()
            print(f"✅ Item criado para Coral: ID {created_item.get('id')}")
            
            # Verificar conversão de mídia
            if "sheet_music_url" in created_item:
                print(f"📄 PDF convertido: {created_item['sheet_music_url']}")
            if "audio_url" in created_item:
                print(f"🎵 Áudio convertido: {created_item['audio_url']}")
                
        else:
            print(f"❌ Erro ao criar item Coral: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 5: Criar item para Orquestra
    try:
        new_item = {
            "type": "Orquestra",
            "title": "Teste Orquestra - Sinfonia nº 5",
            "arrangement": "Beethoven",
            "year": 2024,
            "sheet_music_url": "https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/view",
            "video_url": "https://youtu.be/YWFoYaiGNWM",
            "naipes": ["Violino", "Viola"],
            "grupos": ["Cordas"],
            "active": True
        }
        response = requests.post("http://localhost:8001/api/repertorio/", json=new_item, headers=headers, timeout=10)
        if response.status_code == 200:
            created_item = response.json()
            print(f"✅ Item criado para Orquestra: ID {created_item.get('id')}")
            
            # Verificar conversão de mídia
            if "video_url" in created_item:
                print(f"🎬 Vídeo convertido: {created_item['video_url']}")
                
        else:
            print(f"❌ Erro ao criar item Orquestra: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_media_conversion():
    """Testa conversão de mídia"""
    print("\n🎵 TESTANDO CONVERSÃO DE MÍDIA")
    
    try:
        from utils.media_converter import convert_google_drive_link, convert_youtube_link
        
        # Teste Google Drive Audio
        audio_original = "https://drive.google.com/file/d/1XRwHe9d8jJRqU3DxR49b4dkVID__douV/view"
        audio_converted = convert_google_drive_link(audio_original, "audio")
        print(f"🎵 Áudio: {audio_original} → {audio_converted}")
        
        # Teste Google Drive PDF
        pdf_original = "https://drive.google.com/file/d/1VGXRT8KwcrbxsCiRJb8Izu_GUnQkA662/view"
        pdf_converted = convert_google_drive_link(pdf_original, "pdf")
        print(f"📄 PDF: {pdf_original} → {pdf_converted}")
        
        # Teste YouTube
        video_original = "https://youtu.be/YWFoYaiGNWM"
        video_converted = convert_youtube_link(video_original)
        print(f"🎬 YouTube: {video_original} → {video_converted['embed']}")
        
        print("✅ Conversão de mídia funcionando!")
        
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")

def test_cors():
    """Testa configuração CORS"""
    print("\n🌐 TESTANDO CORS")
    
    try:
        # Teste OPTIONS request
        response = requests.options("http://localhost:8001/api/repertorio/", timeout=5)
        print(f"✅ OPTIONS request: {response.status_code}")
        
        # Verificar headers CORS
        headers = response.headers
        if "Access-Control-Allow-Origin" in headers:
            print(f"✅ CORS Origin: {headers['Access-Control-Allow-Origin']}")
        if "Access-Control-Allow-Methods" in headers:
            print(f"✅ CORS Methods: {headers['Access-Control-Allow-Methods']}")
            
    except Exception as e:
        print(f"❌ Erro CORS: {e}")

def main():
    """Função principal"""
    print("="*60)
    print("🧪 TESTE COMPLETO DO FASTAPI - SETOR MUSICAL MS")
    print("="*60)
    
    # 1. Iniciar servidor
    server_process = start_fastapi_server()
    if not server_process:
        print("❌ Falha ao iniciar servidor. Abortando testes.")
        return
    
    try:
        # 2. Teste de health
        if not test_health_check():
            print("❌ Health check falhou. Abortando testes.")
            return
        
        # 3. Teste de login
        token = test_login()
        if not token:
            print("❌ Login falhou. Abortando testes.")
            return
        
        # 4. Teste de filtros de repertório
        test_repertorio_filters(token)
        
        # 5. Teste de conversão de mídia
        test_media_conversion()
        
        # 6. Teste CORS
        test_cors()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*60)
        
    finally:
        # Parar servidor
        if server_process:
            server_process.terminate()
            print("🛑 Servidor FastAPI parado")

if __name__ == "__main__":
    main()

