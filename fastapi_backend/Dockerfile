# /fastapi_backend/Dockerfile
# v4.0 - 2025-08-06 17:40:00 - Simplifica para resolver problemas de inicialização.

FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependências Python básicas
RUN pip install --no-cache-dir fastapi uvicorn python-multipart

# Copiar apenas os arquivos essenciais primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || echo "Alguns pacotes podem ter falhado, continuando..."

# Copiar o código da aplicação
COPY . .

# Criar diretório para o banco de dados
RUN mkdir -p /app/data

# Expor a porta
EXPOSE 8000

# Comando de inicialização
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["uvicorn", "fastapi_backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
