# fastapi_backend/Dockerfile
# Versão 119 - FINAL com Ordem de Instalação Corrigida

FROM python:3.11-slim

WORKDIR /app

# 1. Instala as dependências do sistema para Playwright
RUN apt-get update && playwright install-deps && rm -rf /var/lib/apt/lists/*

# 2. Copia e instala as dependências Python (incluindo o próprio playwright)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. Agora que o playwright está instalado via pip, instala os navegadores
RUN playwright install

# Copia o código da aplicação
COPY . .

# Cria o diretório de dados para o SQLite
RUN mkdir -p /app/data

EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
