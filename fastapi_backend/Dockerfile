# fastapi_backend/Dockerfile
# Versão 03 - Adiciona a instalação do curl

# Usa uma imagem base oficial do Python.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# ATUALIZAÇÃO: Instala o curl para que o health check do workflow funcione.
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências para o diretório de trabalho.
COPY requirements.txt .

# Instala o pip e as dependências do projeto.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Cria o diretório de dados para o SQLite.
RUN mkdir -p /app/data

# Copia todo o código da aplicação para o diretório de trabalho.
COPY . .

# Expõe a porta 8000 para que o uvicorn possa ser acessado.
EXPOSE 8000

# O comando para iniciar o servidor uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
