# fastapi_backend/Dockerfile
# Versão 02 26/07/2025 12:30

# Usa uma imagem base oficial do Python.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho.
COPY requirements.txt .

# Instala o pip e as dependências do projeto.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# CORREÇÃO: Cria o diretório de dados para o SQLite e define permissões.
RUN mkdir -p /app/data && chown -R www-data:www-data /app/data

# Copia todo o código da aplicação para o diretório de trabalho.
COPY . .

# Expõe a porta 8000 para que o uvicorn possa ser acessado.
EXPOSE 8000

# Define o usuário não-root para rodar a aplicação por segurança.
USER www-data

# O comando para iniciar o servidor uvicorn.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
