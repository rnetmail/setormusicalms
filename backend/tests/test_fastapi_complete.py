# setormusicalms/backend/tests/test_fastapi_complete.py
import pytest
import subprocess
import time
import requests

# --- Test Configuration ---
BASE_URL = "http://localhost:8000"

def stop_fastapi_server(process):
    """Gracefully stops the FastAPI server process."""
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)  # Wait for 5 seconds for the process to terminate
        except subprocess.TimeoutExpired:
            process.kill() # Force kill if it doesn't terminate
        print("\n🔧 Servidor FastAPI parado.")

@pytest.fixture(scope="module")
def fastapi_server():
    """
    A pytest fixture that starts a live FastAPI server for the duration of the tests
    in this module and stops it afterward. 'scope="module"' means it runs once
    per test file.
    """
    print("\n🚀 Iniciando servidor FastAPI para testes de integração...")
    command = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for the server to be ready by polling the root endpoint
    is_ready = False
    for _ in range(20):  # Try for 10 seconds
        try:
            response = requests.get(BASE_URL, timeout=1)
            if response.status_code == 200:
                print("✅ Servidor FastAPI pronto para receber requisições.")
                is_ready = True
                break
        except requests.ConnectionError:
            time.sleep(0.5)
    
    if not is_ready:
        stop_fastapi_server(process)
        pytest.fail("❌ Não foi possível iniciar o servidor FastAPI a tempo.")
        
    yield # This is where the tests will run
    
    # Teardown: Stop the server after tests are done
    stop_fastapi_server(process)

# --- Tests ---

def test_api_is_reachable(fastapi_server):
    """
    Tests if the root endpoint of the live server is reachable and returns the
    expected success code.
    """
    response = requests.get(BASE_URL)
    assert response.status_code == 200

def test_root_returns_welcome_message(fastapi_server):
    """
    Tests if the root endpoint returns the correct welcome message.
    """
    response = requests.get(BASE_URL)
    data = response.json()
    assert "message" in data
    assert "Bem-vindo à API do Setor Musical MS" in data["message"]
