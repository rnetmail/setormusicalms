import pytest
from httpx import AsyncClient

from app.main import app


# O @pytest.mark.asyncio decorator é necessário para rodar testes assíncronos.
# Graças à nossa configuração no pytest.ini, ele agora será executado corretamente.
@pytest.mark.asyncio
async def test_root_endpoint_returns_200_ok():
    """
    Testa se o endpoint raiz ("/") está acessível e retorna o status 200 OK.
    """
    # O AsyncClient permite enviar requisições para a aplicação em memória,
    # sem a necessidade de um servidor rodando. É a forma recomendada de testar.
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_root_endpoint_returns_correct_message():
    """
    Testa se o endpoint raiz ("/") retorna a mensagem de boas-vindas esperada.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")

    response_data = response.json()
    assert "message" in response_data
    assert "API do Setor Musical MS está no ar." in response_data["message"]