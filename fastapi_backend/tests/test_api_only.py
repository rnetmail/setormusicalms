# fastapi_backend/tests/test_api_only.py
# Versão 02 - Com espera pela API

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
    while time.time() - start_time < max_wait:
        try:
            health_response = requests.get(f"{API_URL}/health", timeout=2)
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
        response = requests.get(f"{API_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_repertorio_list(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{API_URL}/repertorio/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_agenda_crud(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        # Adicione aqui os testes de CRUD para a agenda
        response = requests.get(f"{API_URL}/agenda/", headers=headers)
        assert response.status_code == 200
