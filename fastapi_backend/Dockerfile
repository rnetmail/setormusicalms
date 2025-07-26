# fastapi_backend/Dockerfile
# Versão 04 - Adiciona netcat para testes

FROM python:3.11-slim

WORKDIR /app

# ATUALIZAÇÃO: Instala curl (para health checks) e netcat (para esperar a porta)
RUN apt-get update && apt-get install -y curl netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/data
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
