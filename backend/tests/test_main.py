# backend/tests/test_main.py
import pytest
from httpx import AsyncClient

from app.main import app

# @pytest.mark.anyio informa ao Pytest para rodar este teste com o plugin 'anyio'.
# Isso resolve o aviso sobre corotinas não suportadas.
@pytest.mark.anyio
async def test_read_root():
    """
    Testa o endpoint raiz ("/") para garantir que ele retorna a mensagem esperada.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API do Setor Musical MS está no ar."}

