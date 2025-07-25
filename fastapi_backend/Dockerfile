# /fastapi_backend/Dockerfile
# Versão 01 25/07/2025 17:22

# Usa uma imagem Python leve, ideal para produção.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Otimiza os logs do Python em ambientes de contêiner.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia e instala as dependências para aproveitar o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação para dentro do contêiner.
COPY . .

# Expõe a porta que a aplicação vai escutar.
EXPOSE 8000

# O comando para iniciar a aplicação é definido no docker-compose.yml.
# Esta linha é um fallback caso a imagem seja executada sem o Compose.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
