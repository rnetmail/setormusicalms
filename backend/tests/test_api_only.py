# setormusicalms/backend/tests/test_api_only.py
import pytest
from httpx import AsyncClient
from app.main import app  # Import your main FastAPI app instance

# The @pytest.mark.asyncio decorator is necessary for running async test functions
@pytest.mark.asyncio
async def test_root_endpoint():
    """
    Tests the root endpoint ("/") to ensure it's working correctly.
    """
    # AsyncClient allows you to send requests to your app without a running server.
    # It's the recommended way to test async FastAPI applications.
    async with AsyncClient(app=app, base_url="http://test") as client:
        # We 'await' the request since it's an asynchronous operation.
        response = await client.get("/")

    # Assertions to verify the response
    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert "Bem-vindo à API do Setor Musical MS" in response_data["message"]

# You can add more tests for other simple, standalone endpoints here.
# For example, if you had a /health endpoint:
#
# @pytest.mark.asyncio
# async def test_health_check_endpoint():
#     """
#     Tests a hypothetical /health endpoint.
#     """
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}

