# fastapi_backend/tests/test_api_only.py
# Versão 04 - Com Espera de API

import pytest
import requests
import time
from .config import API_URL, ADMIN_USERNAME, ADMIN_PASSWORD

@pytest.fixture(scope="class")
def auth_token(request):
    """
    Fixture que espera a API ficar saudável, faz login uma vez e
    disponibiliza o token para todos os testes da classe.
    """
    # --- Espera pela API ---
    max_wait = 60
    start_time = time.time()
    api_health_url = API_URL.replace("/api", "/api/health")
    while time.time() - start_time < max_wait:
        try:
            health_response = requests.get(api_health_url, timeout=2)
            if health_response.status_code == 200:
                print("\n✅ API está saudável!")
                break
        except requests.ConnectionError:
            time.sleep(2)
    else:
        pytest.fail("API não ficou disponível em 60 segundos.")

    # --- Login ---
    print("Obtendo token de autenticação...")
    login_data = {"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    try:
        response = requests.post(f"{API_URL}/auth/login", data=login_data, timeout=10)
        response.raise_for_status()
        token = response.json().get("access_token")
        assert token, "Token de acesso não foi recebido no login."
        request.cls.token = token
        print("✅ Token obtido com sucesso.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Falha no login da API durante a configuração do teste: {e}")

@pytest.mark.usefixtures("auth_token")
class TestApiOnly:
    token: str

    def test_health_check(self):
        """Testa o endpoint de saúde da API."""
        response = requests.get(API_URL.replace("/api", "/api/health"))
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_repertorio_list_unauthorized(self):
        """Testa se o acesso não autorizado à lista de repertório é negado."""
        response = requests.get(f"{API_URL}/repertorio/")
        assert response.status_code == 401

    def test_repertorio_list_authorized(self):
        """Testa o acesso autorizado à lista de repertório."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{API_URL}/repertorio/?type_filter=Coral", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
