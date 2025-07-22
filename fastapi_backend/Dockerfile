# fastapi_backend/Dockerfile
# Versão 44 17/07/2025 23:20

# Use a imagem oficial do Python como imagem base.
# A versão 'slim' é menor e boa para produção.
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contentor.
WORKDIR /app

# Define variáveis de ambiente para garantir que o Python execute em modo não-bufferizado,
# o que é melhor para logs em contentores.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia primeiro o ficheiro de requisitos para aproveitar o cache do Docker.
# Se o ficheiro não mudar, o Docker reutiliza a camada e não reinstala tudo.
COPY requirements.txt .

# Instala as dependências Python.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação do seu computador para dentro do contentor.
COPY . .

# A porta que a aplicação vai escutar dentro do contentor.
# O docker-compose fará o mapeamento desta porta para a porta 8001 no anfitrião.
EXPOSE 8000

# O comando para iniciar a aplicação é definido no docker-compose.yml,
# então não é estritamente necessário aqui, mas é uma boa prática
# para tornar a imagem executável por si só.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
