# fastapi_backend/tests/test_crud_playwright.py
# Versão 02 - Corrigido para Async

import pytest
from playwright.async_api import async_playwright, Page, expect
from .config import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD

# URL do frontend para os testes de Playwright
FRONTEND_URL = "http://localhost:3000"

@pytest.mark.asyncio
async def test_admin_login_flow(page: Page):
    """Testa o fluxo de login no painel de administração."""
    await page.goto(f"{FRONTEND_URL}/gestao/login")
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('button[type="submit"]')
    # Espera que o dashboard seja carregado, verificando por um elemento específico
    await expect(page.locator('h1:has-text("Painel de Gestão")')).to_be_visible()

@pytest.mark.asyncio
async def test_create_and_delete_repertorio_item(page: Page):
    """Testa a criação e exclusão de um item de repertório."""
    # Login
    await page.goto(f"{FRONTEND_URL}/gestao/login")
    await page.fill('input[name="username"]', ADMIN_USERNAME)
    await page.fill('input[name="password"]', ADMIN_PASSWORD)
    await page.click('button[type="submit"]')
    await expect(page.locator('h1:has-text("Painel de Gestão")')).to_be_visible()

    # Criação
    await page.click('button:has-text("Adicionar Item")')
    await page.fill('input[name="title"]', "Música de Teste Playwright")
    await page.fill('input[name="arranger"]', "Arranjador Teste")
    await page.click('button[type="submit"]')
    
    # Verificação e Exclusão
    item_row = page.locator('tr:has-text("Música de Teste Playwright")')
    await expect(item_row).to_be_visible()
    await item_row.locator('button[aria-label="delete"]').click()
    
    # Confirma que o item foi removido
    await expect(item_row).not_to_be_visible()
