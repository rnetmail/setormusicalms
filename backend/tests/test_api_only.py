# setormusicalms/backend/tests/test_api_only.py
#!/usr/bin/env python3

import requests
import json
from datetime import datetime, date

# Configurações

import pytest
import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
import requests

# Configurações
BASE_URL = "http://127.0.0.1:8000"  # URL base da sua API FastAPI

import subprocess
import time
import requests

# Adicionar path do FastAPI
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        time.sleep(2)
    except Exception:
        pass

def start_fastapi_server():
            if "Uvicorn running on" in line:
                print("✅ Servidor FastAPI iniciado com sucesso!")
                return process
        except Exception:
            time.sleep(1)
    stop_fastapi_server(process)
    raise RuntimeError("❌ Não foi possível iniciar o servidor FastAPI a tempo.")


