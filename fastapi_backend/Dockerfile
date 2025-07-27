# fastapi_backend/Dockerfile
# Versão 118 - FINAL com Dependências do Playwright

FROM python:3.11-slim

WORKDIR /app

# ATUALIZAÇÃO: Instala curl e as dependências de sistema para o Playwright
RUN apt-get update && apt-get install -y curl \
    && playwright install-deps \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instala os navegadores do Playwright
RUN playwright install

# Copia o código da aplicação
COPY . .

# Cria o diretório de dados para o SQLite
RUN mkdir -p /app/data

EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
