# fastapi_backend/Dockerfile
# Versão 120 - Ordem de Instalação Corrigida

FROM python:3.11-slim

WORKDIR /app

# 1. Copia o arquivo de dependências primeiro
COPY requirements.txt .

# 2. Instala as dependências do sistema e do Python (incluindo o próprio playwright)
RUN apt-get update && \
    apt-get install -y curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# 3. Agora que o 'playwright' está instalado via pip, instala as dependências de navegador
RUN playwright install-deps

# 4. Instala os binários dos navegadores do Playwright
RUN playwright install

# Copia o restante do código da aplicação
COPY . .

# Cria o diretório de dados para o SQLite
RUN mkdir -p /app/data

EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
