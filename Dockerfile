# fastapi_backend/Dockerfile
# Versão 06 - FINAL com Dependências do Playwright

FROM python:3.11-slim

WORKDIR /app

# Instala curl e as dependências do sistema para o Playwright
RUN apt-get update && apt-get install -y curl libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libxkbcommon0 libatspi2.0-0 libexpat1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Instala os navegadores do Playwright
RUN playwright install

RUN mkdir -p /app/data
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
