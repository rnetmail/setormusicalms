# fastapi_backend/tests/test_api_only.py
# Versão 37 17/07/2025 22:45
import requests
import pytest
from datetime import datetime, date

# As configurações foram movidas para o topo para fácil acesso.
API_URL = "http://localhost:8001/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Setor@MS25"

# Usamos o decorador de fixture do pytest para criar um "escopo" para a classe de teste.
# 'class' significa que o código dentro do setup será executado uma vez antes de todos os testes na classe.
@pytest.mark.usefixtures("auth_token")
class TestApiOnly:
    """
    Agrupa todos os testes que dependem de um token de autenticação.
    O pytest irá instanciar esta classe e executar cada método 'test_'.
    """

    @pytest.fixture(scope="class")
    def auth_token(self, request):
        """
        Fixture do Pytest para fazer login uma vez e disponibilizar o token 
        para todos os testes da classe através de 'request.cls.token'.
        """
        print("\nObtendo token de autenticação...")
        login_data = {"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        try:
            response = requests.post(f"{API_URL}/auth/login", data=login_data, timeout=10)
            response.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx
            token = response.json().get("access_token")
            assert token, "Token de acesso não foi recebido no login."
            request.cls.token = token
            print("✅ Token obtido com sucesso.")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Falha no login da API durante a configuração do teste: {e}")

    def test_health_check(self):
        """Testa o endpoint de health check da API."""
        print("\nExecutando: test_health_check")
        response = requests.get(f"{API_URL}/health", timeout=5)
        assert response.status_code == 200
        assert response.json().get("status") == "healthy"
        print("✅ Health check passou.")

    def test_repertorio_list(self):
        """Testa a listagem de itens do repertório."""
        print("\nExecutando: test_repertorio_list")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{API_URL}/repertorio/", headers=headers, timeout=10)
        assert response.status_code == 200
        # Verifica se a resposta é uma lista (JSON array)
        assert isinstance(response.json(), list)
        print(f"✅ Listagem de repertório passou. {len(response.json())} itens encontrados.")

    def test_agenda_crud(self):
        """Testa um ciclo completo de CRUD para a Agenda."""
        print("\nExecutando: test_agenda_crud")
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # 1. Criar
        new_item = {
            "group": "Coral",
            "date": date.today().isoformat(),
            "title": f"Evento Teste Pytest {datetime.now().strftime('%H%M%S')}",
            "description": "Descrição do evento de teste via Pytest.",
            "active": True
        }
        response = requests.post(f"{API_URL}/agenda/", json=new_item, headers=headers, timeout=10)
        assert response.status_code == 201, f"Falha ao criar item na agenda: {response.text}"
        created_item = response.json()
        item_id = created_item.get('id')
        print(f"✅ Item da agenda criado com ID: {item_id}")

        # 2. Ler
        response = requests.get(f"{API_URL}/agenda/{item_id}", headers=headers, timeout=10)
        assert response.status_code == 200
        assert response.json()['title'] == new_item['title']
        print(f"✅ Leitura do item {item_id} da agenda passou.")

        # 3. Atualizar
        update_data = {"description": "Descrição atualizada."}
        response = requests.put(f"{API_URL}/agenda/{item_id}", json=update_data, headers=headers, timeout=10)
        assert response.status_code == 200
        assert response.json()['description'] == "Descrição atualizada."
        print(f"✅ Atualização do item {item_id} da agenda passou.")

        # 4. Apagar
        response = requests.delete(f"{API_URL}/agenda/{item_id}", headers=headers, timeout=10)
        assert response.status_code == 204
        print(f"✅ Remoção do item {item_id} da agenda passou.")

        # 5. Verificar se foi apagado
        response = requests.get(f"{API_URL}/agenda/{item_id}", headers=headers, timeout=10)
        assert response.status_code == 404
        print(f"✅ Verificação de remoção do item {item_id} passou.")
