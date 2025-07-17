# fastapi_backend/tests/test_crud_playwright.py
# Versão 38 17/07/2025 22:48
import pytest
import asyncio
from playwright.async_api import async_playwright, Page, Browser

# As configurações foram movidas para o topo para fácil acesso.
BASE_URL = "http://localhost:8001"  # Assumindo que o Nginx do docker-compose está a rodar aqui
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

# Marca toda a classe para ser executada com o plugin pytest-asyncio
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
        await page.goto(f"{BASE_URL}/#/gestao/login", timeout=30000)
        
        # Preenche as credenciais
        await page.fill('input[name="username"]', ADMIN_USERNAME)
        await page.fill('input[name="password"]', ADMIN_PASSWORD)
        
        # Clica no botão de login
        await page.click('button[type="submit"]')
        
        # Espera pela navegação para o dashboard
        await page.wait_for_url(f"{BASE_URL}/#/gestao", timeout=10000)
        
        # Verifica se um elemento do dashboard está visível
        dashboard_title = await page.locator("h1:has-text('Painel de Gestão')").is_visible()
        assert dashboard_title, "Não foi possível encontrar o título do 'Painel de Gestão' após o login."
        print("✅ Login no painel de gestão realizado com sucesso.")

    async def test_create_and_delete_repertorio_item(self, page: Page):
        """Testa a criação e remoção de um item de repertório no painel de gestão."""
        print("\nExecutando: test_create_and_delete_repertorio_item")
        
        # Primeiro, faz o login (poderia ser uma fixture separada)
        await page.goto(f"{BASE_URL}/#/gestao/login")
        await page.fill('input[name="username"]', ADMIN_USERNAME)
        await page.fill('input[name="password"]', ADMIN_PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_url(f"{BASE_URL}/#/gestao")
        print("Login para o teste de CRUD realizado.")

        # Navega para a aba do Coral e clica em Adicionar Novo
        await page.click("button:has-text('Coral')")
        await page.click("button:has-text('Adicionar Novo')")

        # Preenche o formulário para um novo item de repertório
        item_title = f"Teste Playwright {datetime.now().strftime('%H%M%S')}"
        await page.wait_for_selector('input[name="title"]')
        await page.fill('input[name="title"]', item_title)
        await page.fill('input[name="year"]', "2025")
        await page.fill('input[name="sheetMusicUrl"]', "http://exemplo.com/partitura.pdf")
        
        # Salva o novo item
        await page.click("button:has-text('Salvar')")
        
        # Verifica se o item aparece na tabela
        await page.wait_for_selector(f"text={item_title}", timeout=5000)
        print(f"✅ Item '{item_title}' criado com sucesso e visível na tabela.")

        # Encontra a linha do item criado e clica no ícone de apagar
        item_row = page.locator("tr", has_text=item_title)
        
        # Aceita a confirmação do browser
        page.on("dialog", lambda dialog: dialog.accept())
        
        await item_row.locator('button[aria-label*="delete"], button:has-text("Excluir")').click()
        
        # Espera que o item desapareça da UI
        await page.wait_for_timeout(2000) # Espera para a UI atualizar
        item_is_visible = await page.locator(f"text={item_title}").is_visible()
        assert not item_is_visible, "O item ainda estava visível após ser apagado."
        print(f"✅ Item '{item_title}' apagado com sucesso.")
