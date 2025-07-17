# fastapi_backend/tests/test_crud_playwright.py
# Versão 61 18/07/2025 00:12
import pytest
import asyncio
from playwright.async_api import async_playwright, Page, Browser
from datetime import datetime

BASE_URL = "http://localhost"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

@pytest.mark.asyncio
class TestCrudPlaywright:
    @pytest.fixture(scope="class", autouse=True)
    async def browser_setup(self):
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=True, slow_mo=50)
            yield
            await self.browser.close()

    # CORREÇÃO: A fixture agora é uma função 'async' e usa 'yield'
    # para passar o controlo para o teste e depois limpar.
    @pytest.fixture(scope="function")
    async def page(self) -> Page:
        page = await self.browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        yield page
        await page.close()

    async def test_admin_login(self, page: Page):
        """Testa o fluxo de login no painel de gestão."""
        print("\nExecutando: test_admin_login")
        await page.goto(f"{BASE_URL}/#/gestao/login", timeout=30000)
        
        await page.fill('input[name="username"]', ADMIN_USERNAME)
        await page.fill('input[name="password"]', ADMIN_PASSWORD)
        
        await page.click('button[type="submit"]')
        
        await page.wait_for_url(f"{BASE_URL}/#/gestao", timeout=10000)
        
        dashboard_title = await page.locator("h1:has-text('Painel de Gestão')").is_visible()
        assert dashboard_title, "Não foi possível encontrar o título do 'Painel de Gestão' após o login."
        print("✅ Login no painel de gestão realizado com sucesso.")

    async def test_create_and_delete_repertorio_item(self, page: Page):
        """Testa a criação e remoção de um item de repertório no painel de gestão."""
        print("\nExecutando: test_create_and_delete_repertorio_item")
        
        await self.test_admin_login(page) # Reutiliza a função de login
        print("Login para o teste de CRUD realizado.")

        await page.click("button:has-text('Coral')")
        await page.click("button:has-text('Adicionar Novo')")

        item_title = f"Teste Playwright {datetime.now().strftime('%H%M%S')}"
        await page.wait_for_selector('input[name="title"]')
        await page.fill('input[name="title"]', item_title)
        await page.fill('input[name="year"]', "2025")
        await page.fill('input[name="sheetMusicUrl"]', "http://exemplo.com/partitura.pdf")
        
        await page.click("button:has-text('Salvar')")
        
        await page.wait_for_selector(f"text={item_title}", timeout=5000)
        print(f"✅ Item '{item_title}' criado com sucesso e visível na tabela.")

        item_row = page.locator("tr", has_text=item_title)
        
        page.on("dialog", lambda dialog: dialog.accept())
        
        # O seletor do botão de apagar pode variar, vamos usar um mais genérico
        await item_row.locator('button:has([d*="M9 2a1"])').click()
        
        await page.wait_for_timeout(2000)
        item_is_visible = await page.locator(f"text={item_title}").is_visible()
        assert not item_is_visible, "O item ainda estava visível após ser apagado."
        print(f"✅ Item '{item_title}' apagado com sucesso.")
