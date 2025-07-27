# fastapi_backend/Dockerfile
# Versão 117 - FINAL PARA O BACKEND (Python + FastAPI)

FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema para o Playwright funcionar
RUN apt-get update && apt-get install -y curl libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libxkbcommon0 libatspi2.0-0 libexpat1 && rm -rf /var/lib/apt/lists/*

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
