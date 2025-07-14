#!/usr/bin/env python3
"""
Script de testes automatizados com Playwright para validar CRUDs
"""
import asyncio
import json
import sys
import os
from datetime import datetime
from playwright.async_api import async_playwright, Page, Browser
import requests
import time

# Configurações
BASE_URL = "https://setormusicalms.art.br"
API_URL = "http://localhost:8001/api"  # FastAPI local
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

class CRUDTester:
    def __init__(self):
        self.browser = None
        self.page = None
        self.auth_token = None
        self.test_results = []
        
    async def setup(self):
        """Configuração inicial do teste"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()
        
        # Configurar viewport
        await self.page.set_viewport_size({"width": 1280, "height": 720})
        
        print("🚀 Iniciando testes automatizados dos CRUDs...")
        
    async def teardown(self):
        """Limpeza após os testes"""
        if self.browser:
            await self.browser.close()
            
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
            
    async def test_api_health(self):
        """Testa se a API está funcionando"""
        try:
            response = requests.get(f"{API_URL}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("API Health Check", "PASS", "API respondendo corretamente")
                return True
            else:
                self.log_test("API Health Check", "FAIL", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health Check", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_api_login(self):
        """Testa login via API"""
        try:
            login_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            response = requests.post(f"{API_URL}/auth/login", data=login_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("access_token")
                self.log_test("API Login", "PASS", f"Token obtido: {self.auth_token[:20]}...")
                return True
            else:
                self.log_test("API Login", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("API Login", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_website_access(self):
        """Testa acesso ao site principal"""
        try:
            await self.page.goto(BASE_URL, timeout=30000)
            await self.page.wait_for_load_state("networkidle")
            
            title = await self.page.title()
            if "Setor Musical" in title:
                self.log_test("Website Access", "PASS", f"Título: {title}")
                return True
            else:
                self.log_test("Website Access", "FAIL", f"Título inesperado: {title}")
                return False
        except Exception as e:
            self.log_test("Website Access", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_admin_panel_access(self):
        """Testa acesso ao painel administrativo"""
        try:
            # Navegar para área de gestão
            await self.page.goto(f"{BASE_URL}/#/gestao", timeout=30000)
            await self.page.wait_for_load_state("networkidle")
            
            # Verificar se chegou na página de gestão
            await self.page.wait_for_selector("text=Painel de Gestão", timeout=10000)
            self.log_test("Admin Panel Access", "PASS", "Painel administrativo acessível")
            return True
        except Exception as e:
            self.log_test("Admin Panel Access", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_users_crud_ui(self):
        """Testa CRUD de usuários via interface"""
        try:
            # Clicar na aba Usuários
            await self.page.click("text=Usuários")
            await self.page.wait_for_timeout(2000)
            
            # Verificar se a lista de usuários carregou
            users_section = await self.page.wait_for_selector("text=Usuários", timeout=5000)
            if users_section:
                self.log_test("Users CRUD - List", "PASS", "Lista de usuários carregada")
            
            # Tentar criar novo usuário
            await self.page.click("text=Adicionar Novo")
            await self.page.wait_for_timeout(1000)
            
            # Preencher formulário
            await self.page.fill("input[placeholder*='usuário'], input[type='text']:first-of-type", "teste_playwright")
            await self.page.fill("input[placeholder*='senha'], input[type='password']:first-of-type", "teste123")
            await self.page.fill("input[placeholder*='confirme'], input[type='password']:last-of-type", "teste123")
            
            # Tentar salvar
            await self.page.click("button:has-text('Salvar')")
            await self.page.wait_for_timeout(3000)
            
            # Verificar se o modal fechou (indicando sucesso)
            modal_visible = await self.page.is_visible("text=Adicionar Usuário")
            if not modal_visible:
                self.log_test("Users CRUD - Create", "PASS", "Usuário criado com sucesso")
            else:
                self.log_test("Users CRUD - Create", "FAIL", "Modal ainda visível após salvar")
                
            return True
        except Exception as e:
            self.log_test("Users CRUD - UI", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_repertorio_crud_ui(self):
        """Testa CRUD de repertório via interface"""
        try:
            # Navegar para aba Coral
            await self.page.click("text=Coral")
            await self.page.wait_for_timeout(2000)
            
            # Verificar se a seção carregou
            coral_section = await self.page.wait_for_selector("text=Repertório", timeout=5000)
            if coral_section:
                self.log_test("Repertorio CRUD - Access", "PASS", "Seção de repertório acessível")
            
            return True
        except Exception as e:
            self.log_test("Repertorio CRUD - UI", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_api_users_crud(self):
        """Testa CRUD de usuários via API"""
        if not self.auth_token:
            self.log_test("API Users CRUD", "SKIP", "Token não disponível")
            return False
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            # Listar usuários
            response = requests.get(f"{API_URL}/users/", headers=headers, timeout=10)
            if response.status_code == 200:
                users = response.json()
                self.log_test("API Users - List", "PASS", f"Encontrados {len(users)} usuários")
            else:
                self.log_test("API Users - List", "FAIL", f"Status: {response.status_code}")
                
            # Criar usuário
            new_user = {
                "username": "teste_api",
                "email": "teste@api.com",
                "password": "teste123",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False
            }
            response = requests.post(f"{API_URL}/users/", json=new_user, headers=headers, timeout=10)
            if response.status_code == 200:
                created_user = response.json()
                self.log_test("API Users - Create", "PASS", f"Usuário criado com ID: {created_user.get('id')}")
            else:
                self.log_test("API Users - Create", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                
            return True
        except Exception as e:
            self.log_test("API Users CRUD", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def test_api_repertorio_crud(self):
        """Testa CRUD de repertório via API"""
        if not self.auth_token:
            self.log_test("API Repertorio CRUD", "SKIP", "Token não disponível")
            return False
            
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            # Listar itens do repertório
            response = requests.get(f"{API_URL}/repertorio/", headers=headers, timeout=10)
            if response.status_code == 200:
                items = response.json()
                self.log_test("API Repertorio - List", "PASS", f"Encontrados {len(items)} itens")
            else:
                self.log_test("API Repertorio - List", "FAIL", f"Status: {response.status_code}")
                
            # Criar item do repertório
            new_item = {
                "type": "Coral",
                "title": "Teste Playwright",
                "year": 2024,
                "sheet_music_url": "https://example.com/partitura.pdf",
                "active": True
            }
            response = requests.post(f"{API_URL}/repertorio/", json=new_item, headers=headers, timeout=10)
            if response.status_code == 200:
                created_item = response.json()
                self.log_test("API Repertorio - Create", "PASS", f"Item criado com ID: {created_item.get('id')}")
            else:
                self.log_test("API Repertorio - Create", "FAIL", f"Status: {response.status_code}, Response: {response.text}")
                
            return True
        except Exception as e:
            self.log_test("API Repertorio CRUD", "FAIL", f"Erro: {str(e)}")
            return False
            
    async def run_all_tests(self):
        """Executa todos os testes"""
        await self.setup()
        
        try:
            # Testes de infraestrutura
            await self.test_api_health()
            await self.test_website_access()
            
            # Testes de autenticação
            await self.test_api_login()
            await self.test_admin_panel_access()
            
            # Testes de CRUD via UI
            await self.test_users_crud_ui()
            await self.test_repertorio_crud_ui()
            
            # Testes de CRUD via API
            await self.test_api_users_crud()
            await self.test_api_repertorio_crud()
            
        finally:
            await self.teardown()
            
        # Gerar relatório
        self.generate_report()
        
    def generate_report(self):
        """Gera relatório dos testes"""
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        skipped_tests = len([t for t in self.test_results if t["status"] == "SKIP"])
        
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("="*60)
        print(f"Total de testes: {total_tests}")
        print(f"✅ Passou: {passed_tests}")
        print(f"❌ Falhou: {failed_tests}")
        print(f"⏭️ Pulado: {skipped_tests}")
        print(f"📈 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        print("="*60)
        
        # Salvar relatório em arquivo
        report_file = f"/home/ubuntu/test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "skipped": skipped_tests,
                    "success_rate": (passed_tests/total_tests)*100
                },
                "tests": self.test_results
            }, f, indent=2)
            
        print(f"📄 Relatório salvo em: {report_file}")

async def main():
    """Função principal"""
    tester = CRUDTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

