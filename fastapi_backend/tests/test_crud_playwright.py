# fastapi_backend/tests/test_crud_playwright.py
# Versão 29 18/07/2025 00:30
import pytest
from playwright.async_api import async_playwright, Page
from datetime import datetime

# O endereço base para os testes de frontend.
BASE_URL = "http://localhost:3000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

# CORREÇÃO: O decorador @pytest.mark.asyncio foi removido.
# O pytest-playwright gere o seu próprio loop de eventos e o decorador causa um conflito.
class TestCrudPlaywright:
    @pytest.fixture(scope="class", autouse=True)
    async def browser_context_setup(self, playwright: async_playwright):
        """Inicia uma instância do browser para todos os testes da classe."""
        self.browser = await playwright.chromium.launch(headless=True, slow_mo=50)
        yield
        await self.browser.close()

    async def admin_login(self, page: Page):
        """Função auxiliar para realizar o login no painel de gestão."""
        await page.goto(f"{BASE_URL}/#/gestao/login", timeout=30000)
        await page.fill('input[name="username"]', ADMIN_USERNAME)
        await page.fill('input[name="password"]', ADMIN_PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_url(f"{BASE_URL}/#/gestao", timeout=10000)
        assert await page.locator("h1:has-text('Painel de Gestão')").is_visible()

    async def test_admin_login_flow(self):
        """Testa o fluxo de login no painel de gestão."""
        page = await self.browser.new_page()
        try:
            await self.admin_login(page)
        finally:
            await page.close()

    async def test_create_and_delete_repertorio_item(self):
        """Testa a criação e remoção de um item de repertório através da UI."""
        page = await self.browser.new_page()
        try:
            await self.admin_login(page)
            
            await page.
