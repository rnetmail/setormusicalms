# fastapi_backend/tests/test_crud_playwright.py
# Versão 08 - FINAL sem Conflito de Loop

import pytest
from playwright.async_api import Page, expect
from .config import ADMIN_USERNAME, ADMIN_PASSWORD

# A URL do frontend DENTRO da rede Docker é o nome do serviço na porta interna
# que o servidor 'serve' está usando, conforme o Dockerfile do frontend.
FRONTEND_URL = "http://frontend:3000"

# NOTA: O decorador @pytest.mark.asyncio foi removido.
# O pytest-playwright gerencia o loop de eventos para seus próprios testes.
async def test_admin_login_flow(page: Page):
    """Testa o fluxo de login no painel de administração."""
    await page.goto(f"{FRONTEND_URL}/gestao/login")
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('button[type="submit"]')
    await expect(page.locator('h1:has-text("Painel de Gestão")')).to_be_visible()

async def test_create_and_delete_repertorio_item(page: Page):
    """Testa a criação e exclusão de um item de repertório."""
    # Login
    await page.goto(f"{FRONTEND_URL}/gestao/login")
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('button[type="submit"]')
    await expect(page.locator('h1:has-text("Painel de Gestão")')).to_be_visible()

    # Navega para a aba correta e clica para adicionar
    await page.click('button[role="tab"]:has-text("Coral")')
    await page.click('button:has-text("Adicionar Item")')
    
    # Preenche o formulário de criação
    await page.fill('input[name="title"]', "Música de Teste Playwright")
    await page.fill('input[name="arranger"]', "Arranjador Teste")
    await page.click('button[type="submit"]')
    
    # Verificação e Exclusão
    item_row = page.locator('tr:has-text("Música de Teste Playwright")')
    await expect(item_row).to_be_visible()
    await item_row.locator('button[aria-label="delete"]').click()
    
    # Confirma que o item foi removido
    await expect(item_row).not_to_be_visible()
