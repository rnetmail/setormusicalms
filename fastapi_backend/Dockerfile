# fastapi_backend/Dockerfile
# Versão 05 - FINAL COM AMBIENTE DE TESTE EMBUTIDO

FROM python:3.11-slim

WORKDIR /app

# Instala o curl para health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e instala tudo (app + teste)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instala os navegadores do Playwright dentro da imagem
RUN playwright install

# Cria o diretório de dados para o SQLite
RUN mkdir -p /app/data

# Copia o código da aplicação
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
