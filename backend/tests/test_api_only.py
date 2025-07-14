#!/usr/bin/env python3
"""
Script de testes focado apenas na API FastAPI
"""
import requests
import json
import sys
import os
from datetime import datetime, date

# Configurações
API_URL = "http://localhost:8001/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

class APITester:
    def __init__(self):
        self.auth_token = None
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Registra resultado do teste"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
            
    def test_health(self):
        """Testa endpoint de health"""
        try:
            response = requests.get(f"{API_URL}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", "PASS", f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Health Check", "FAIL", f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", "FAIL", f"Erro: {str(e)}")
            return False
            
    def test_login(self):
        """Testa login e obtenção de token"""
        try:
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            response = requests.post(f"{API_URL}/auth/login", data=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                self.log_test("Login", "PASS", f"Token obtido: {self.auth_token[:20]}...")
                return True
            else:
                self.log_test("Login", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Login", "FAIL", f"Erro: {str(e)}")
            return False
            
    def get_headers(self):
        """Retorna headers com autenticação"""
        if not self.auth_token:
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}
        
    def test_users_crud(self):
        """Testa CRUD completo de usuários"""
        headers = self.get_headers()
        if not headers:
            self.log_test("Users CRUD", "SKIP", "Token não disponível")
            return False
            
        try:
            # 1. Listar usuários
            response = requests.get(f"{API_URL}/users/", headers=headers, timeout=10)
            if response.status_code == 200:
                users = response.json()
                self.log_test("Users - List", "PASS", f"Encontrados {len(users)} usuários")
            else:
                self.log_test("Users - List", "FAIL", f"Status: {response.status_code}")
                return False
                
            # 2. Criar usuário
            new_user = {
                "username": f"teste_api_{datetime.now().strftime('%H%M%S')}",
                "email": f"teste_{datetime.now().strftime('%H%M%S')}@api.com",
                "password": "teste123",
                "first_name": "Teste",
                "last_name": "API",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False
            }
            response = requests.post(f"{API_URL}/users/", json=new_user, headers=headers, timeout=10)
            if response.status_code == 200:
                created_user = response.json()
                user_id = created_user.get('id')
                self.log_test("Users - Create", "PASS", f"Usuário criado com ID: {user_id}")
                
                # 3. Buscar usuário específico
                response = requests.get(f"{API_URL}/users/{user_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Users - Read", "PASS", f"Usuário {user_id} encontrado")
                else:
                    self.log_test("Users - Read", "FAIL", f"Status: {response.status_code}")
                    
                # 4. Atualizar usuário
                update_data = {"first_name": "Teste Atualizado"}
                response = requests.put(f"{API_URL}/users/{user_id}", json=update_data, headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Users - Update", "PASS", f"Usuário {user_id} atualizado")
                else:
                    self.log_test("Users - Update", "FAIL", f"Status: {response.status_code}")
                    
                # 5. Deletar usuário
                response = requests.delete(f"{API_URL}/users/{user_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Users - Delete", "PASS", f"Usuário {user_id} deletado")
                else:
                    self.log_test("Users - Delete", "FAIL", f"Status: {response.status_code}")
                    
            else:
                self.log_test("Users - Create", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                return False
                
            return True
        except Exception as e:
            self.log_test("Users CRUD", "FAIL", f"Erro: {str(e)}")
            return False
            
    def test_repertorio_crud(self):
        """Testa CRUD completo de repertório"""
        headers = self.get_headers()
        if not headers:
            self.log_test("Repertorio CRUD", "SKIP", "Token não disponível")
            return False
            
        try:
            # 1. Listar itens
            response = requests.get(f"{API_URL}/repertorio/", headers=headers, timeout=10)
            if response.status_code == 200:
                items = response.json()
                self.log_test("Repertorio - List", "PASS", f"Encontrados {len(items)} itens")
            else:
                self.log_test("Repertorio - List", "FAIL", f"Status: {response.status_code}")
                return False
                
            # 2. Criar item
            new_item = {
                "type": "Coral",
                "title": f"Teste API {datetime.now().strftime('%H:%M:%S')}",
                "arrangement": "Arranjo Teste",
                "year": 2024,
                "sheet_music_url": "https://example.com/partitura.pdf",
                "audio_url": "https://example.com/audio.mp3",
                "naipes": ["Soprano", "Contralto"],
                "grupos": ["Grupo 1"],
                "active": True
            }
            response = requests.post(f"{API_URL}/repertorio/", json=new_item, headers=headers, timeout=10)
            if response.status_code == 200:
                created_item = response.json()
                item_id = created_item.get('id')
                self.log_test("Repertorio - Create", "PASS", f"Item criado com ID: {item_id}")
                
                # 3. Buscar item específico
                response = requests.get(f"{API_URL}/repertorio/{item_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Repertorio - Read", "PASS", f"Item {item_id} encontrado")
                else:
                    self.log_test("Repertorio - Read", "FAIL", f"Status: {response.status_code}")
                    
                # 4. Atualizar item
                update_data = {"title": "Título Atualizado via API"}
                response = requests.put(f"{API_URL}/repertorio/{item_id}", json=update_data, headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Repertorio - Update", "PASS", f"Item {item_id} atualizado")
                else:
                    self.log_test("Repertorio - Update", "FAIL", f"Status: {response.status_code}")
                    
                # 5. Deletar item
                response = requests.delete(f"{API_URL}/repertorio/{item_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Repertorio - Delete", "PASS", f"Item {item_id} deletado")
                else:
                    self.log_test("Repertorio - Delete", "FAIL", f"Status: {response.status_code}")
                    
            else:
                self.log_test("Repertorio - Create", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                return False
                
            return True
        except Exception as e:
            self.log_test("Repertorio CRUD", "FAIL", f"Erro: {str(e)}")
            return False
            
    def test_agenda_crud(self):
        """Testa CRUD completo de agenda"""
        headers = self.get_headers()
        if not headers:
            self.log_test("Agenda CRUD", "SKIP", "Token não disponível")
            return False
            
        try:
            # 1. Listar itens
            response = requests.get(f"{API_URL}/agenda/", headers=headers, timeout=10)
            if response.status_code == 200:
                items = response.json()
                self.log_test("Agenda - List", "PASS", f"Encontrados {len(items)} itens")
            else:
                self.log_test("Agenda - List", "FAIL", f"Status: {response.status_code}")
                return False
                
            # 2. Criar item
            new_item = {
                "group": "Coral",
                "date": date.today().isoformat(),
                "title": f"Evento Teste {datetime.now().strftime('%H:%M:%S')}",
                "description": "Descrição do evento de teste via API",
                "active": True
            }
            response = requests.post(f"{API_URL}/agenda/", json=new_item, headers=headers, timeout=10)
            if response.status_code == 200:
                created_item = response.json()
                item_id = created_item.get('id')
                self.log_test("Agenda - Create", "PASS", f"Item criado com ID: {item_id}")
                
                # 3. Deletar item (limpeza)
                response = requests.delete(f"{API_URL}/agenda/{item_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Agenda - Delete", "PASS", f"Item {item_id} deletado")
                    
            else:
                self.log_test("Agenda - Create", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                return False
                
            return True
        except Exception as e:
            self.log_test("Agenda CRUD", "FAIL", f"Erro: {str(e)}")
            return False
            
    def test_recados_crud(self):
        """Testa CRUD completo de recados"""
        headers = self.get_headers()
        if not headers:
            self.log_test("Recados CRUD", "SKIP", "Token não disponível")
            return False
            
        try:
            # 1. Listar itens
            response = requests.get(f"{API_URL}/recados/", headers=headers, timeout=10)
            if response.status_code == 200:
                items = response.json()
                self.log_test("Recados - List", "PASS", f"Encontrados {len(items)} itens")
            else:
                self.log_test("Recados - List", "FAIL", f"Status: {response.status_code}")
                return False
                
            # 2. Criar item
            new_item = {
                "group": "Setor",
                "date": date.today().isoformat(),
                "title": f"Recado Teste {datetime.now().strftime('%H:%M:%S')}",
                "description": "Descrição do recado de teste via API",
                "active": True
            }
            response = requests.post(f"{API_URL}/recados/", json=new_item, headers=headers, timeout=10)
            if response.status_code == 200:
                created_item = response.json()
                item_id = created_item.get('id')
                self.log_test("Recados - Create", "PASS", f"Item criado com ID: {item_id}")
                
                # 3. Deletar item (limpeza)
                response = requests.delete(f"{API_URL}/recados/{item_id}", headers=headers, timeout=10)
                if response.status_code == 200:
                    self.log_test("Recados - Delete", "PASS", f"Item {item_id} deletado")
                    
            else:
                self.log_test("Recados - Create", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                return False
                
            return True
        except Exception as e:
            self.log_test("Recados CRUD", "FAIL", f"Erro: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes da API FastAPI...")
        print("="*60)
        
        # Testes básicos
        self.test_health()
        self.test_login()
        
        # Testes de CRUD
        self.test_users_crud()
        self.test_repertorio_crud()
        self.test_agenda_crud()
        self.test_recados_crud()
        
        # Gerar relatório
        self.generate_report()
        
    def generate_report(self):
        """Gera relatório dos testes"""
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        skipped_tests = len([t for t in self.test_results if t["status"] == "SKIP"])
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DOS TESTES DA API")
        print("="*60)
        print(f"Total de testes: {total_tests}")
        print(f"✅ Passou: {passed_tests}")
        print(f"❌ Falhou: {failed_tests}")
        print(f"⏭️ Pulado: {skipped_tests}")
        if total_tests > 0:
            print(f"📈 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        print("="*60)
        
        # Salvar relatório em arquivo
        report_file = f"/home/ubuntu/api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "skipped": skipped_tests,
                    "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0
                },
                "tests": self.test_results
            }, f, indent=2)
            
        print(f"📄 Relatório salvo em: {report_file}")

def main():
    """Função principal"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()

