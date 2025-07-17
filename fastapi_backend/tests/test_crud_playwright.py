# fastapi_backend/tests/test_crud_playwright.py
# Versão 60 18/07/2025 00:10
import pytest
import asyncio
from playwright.async_api import async_playwright, Page, Browser
from datetime import datetime

# CORREÇÃO: A URL base para os testes de frontend deve ser a porta 80,
# que é onde o contentor do Nginx está exposto.
BASE_URL = "http://localhost"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

@pytest.mark.asyncio
class TestCrudPlaywright:
    """
    Agrupa os testes de ponta a ponta (E2E) que usam Playwright
    para interagir com a interface do utilizador.
    """

    @pytest.fixture(scope="class", autouse=True)
    async def browser_setup(self):
        """
        Fixture que inicializa o browser uma vez para todos os testes da classe
        e o fecha no final.
        """
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=True, slow_mo=50)
            yield
            await self.browser.close()

    @pytest.fixture(scope="function")
    async def page(self) -> Page:
        """
        Fixture que cria uma nova página para cada teste, garantindo o isolamento.
        """
        page = await self.browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        yield page
        await page.close()

    async def test_admin_login(self, page: Page):
        """Testa o fluxo de login no painel de gestão."""
        print("\nExecutando: test_admin_login")
        # O #/gestao/login é por causa do HashRouter do React
        await page.goto(f"{BASE_URL}/#/gestao/login", timeout=30000)
        
        await page.fill('input[name="username"]', ADMIN_USERNAME)
        await page.fill('input[name="password"]', ADMIN_PASSWORD)
        
        await page.click('button[type="submit"]')
        
        await page.wait_for_url(f"{BASE_URL}/#/gestao", timeout=10000)
        
        dashboard_title = await page.locator("h1:has-text('Painel de Gestão')").is_visible()
        assert dashboard_title, "Não foi possível encontrar o título do 'Painel de Gestão' após o login."
        print("✅ Login no painel de gestão realizado com sucesso.")
