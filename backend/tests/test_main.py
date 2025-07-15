# backend/tests/test_main.py
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

# @pytest.mark.anyio informa ao Pytest para rodar este teste com o plugin 'anyio'.
@pytest.mark.anyio
async def test_read_root():
    """
    Testa o endpoint raiz ("/") para garantir que ele retorna a mensagem esperada.
    """
    # A nova forma recomendada de usar o AsyncClient para testes em memória.
    # Isso resolve o DeprecationWarning.
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API do Setor Musical MS está no ar."}
