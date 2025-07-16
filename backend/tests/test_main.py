import json
import pytest
from httpx import AsyncClient
from tests.factories import UserFactory  # Importe a factory
from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash  # Importe as funções de segurança

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

@pytest.mark.asyncio
async def test_create_user(db_session: Session):   # Use a fixture db_session
    """
    Testa o endpoint de criação de usuário (POST /users/).
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Cria um usuário usando a factory
        user_data = UserFactory.build()
        
        # Envia a requisição POST com os dados do usuário
        response = await client.post("/users/", json=user_data.__dict__)
        response_data = response.json()

        # Verifica se a requisição foi bem-sucedida (código 201 Created)
        assert response.status_code == 201

        # Verifica se os dados retornados correspondem aos dados enviados
        assert response_data["username"] == user_data.username
        assert response_data["email"] == user_data.email
        # Verifique outros campos, como ID (se gerado pela API e presente no modelo)

        # Teste de integração: verifique se o usuário foi persistido no banco de dados
        from app import models  # Importe seus modelos SQLAlchemy
        persisted_user = db_session.query(models.User).filter(models.User.email == user_data.email).first()
        assert persisted_user is not None
        assert persisted_user.username == user_data.username
        assert persisted_user.email == user_data.email

@pytest.mark.asyncio
async def test_create_user_invalid_data():
    """
    Testa o endpoint de criação de usuário (POST /users/) com dados inválidos.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Envia uma requisição POST com dados inválidos (email faltando)
        response = await client.post("/users/", json={"username": "testuser"})

        # Verifica se a API retorna o código de erro apropriado (422 Unprocessable Entity)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_success(db_session: Session):
    """
    Testa o login com credenciais válidas e verifica se o token é retornado.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Cria um usuário para o teste de login
        user_data = UserFactory.create()  
        from app import models  # Importe seus modelos SQLAlchemy
        # Cria o usuario no banco de dados
        user_data.hashed_password = get_password_hash("password_segura")  # Use a função de hash
        # Cria o usuário no banco de dados
        user = models.User(**user_data.__dict__)
        db_session.add(user)
        db_session.commit()
        # Dados para login (substitua com os campos de login da sua aplicação)
        login_data = {"username": user_data.username, "password": "password_segura"}
        # Envia a requisição de login
        response = await client.post("/token", data=login_data)
        # Verifica se o login foi bem-sucedido (código 200 OK)
        assert response.status_code == 200
        # Verifica se o token foi retornado
        response_json = response.json()
        assert "access_token" in response_json
        assert "token_type" in response_json
        # (Opcional) Valide o formato do token, se for um JWT
        # assert response_json["token_type"] == "bearer"  # Ou outro tipo, se aplicável

@pytest.mark.asyncio
async def test_login_failure(db_session: Session):
    """
    Testa o login com credenciais inválidas e verifica se o erro é retornado.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Dados para login inválidos
        login_data = {"username": "wronguser", "password": "wrongpassword"}
        # Envia a requisição de login
        response = await client.post("/token", data=login_data)
        # Verifica se o login falhou (código 401 Unauthorized)
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_authenticated_access(db_session: Session):
    """Testa o acesso a um endpoint autenticado com um token válido."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Cria um usuário para o teste
        user_data = UserFactory.create()
        user_data.hashed_password = get_password_hash("password_segura")
        from app import models
        user = models.User(**user_data.__dict__)
        db_session.add(user)
        db_session.commit()

        # Faz login para obter o token
        login_data = {"username": user_data.username, "password": "password_segura"}
        login_response = await client.post("/token", data=login_data)
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Opcional: Validar o token (JWT, etc.) antes de usar

        # Envia uma requisição para um endpoint autenticado (substitua '/protected' pelo seu endpoint)
        response = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

        # Verifica se o acesso foi bem-sucedido (código 200 OK ou outro código de sucesso)
        assert response.status_code == 200
        # (Opcional) Verifica se os dados do usuário autenticado são retornados corretamente
        # assert response.json()["username"] == "testuser" # Ajuste conforme a resposta do seu endpoint

@pytest.mark.asyncio
async def test_create_user_invalid_data():
    """
    Testa o endpoint de criação de usuário (POST /users/) com dados inválidos.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Envia uma requisição POST com dados inválidos (email faltando)
        response = await client.post("/users/", json={"username": "testuser"})

        # Verifica se a API retorna o código de erro apropriado (422 Unprocessable Entity)
        assert response.status_code == 422