# /fastapi_backend/Dockerfile
# v11 - 2025-07-30 02:10:00 - Otimiza o cache de camadas e a ordem de instalação.

# Etapa 1: Definir a imagem base
# Usar uma imagem 'slim' é uma boa prática para manter o tamanho final reduzido.
FROM python:3.11-slim

# Etapa 2: Definir o diretório de trabalho
# Todos os comandos subsequentes serão executados a partir deste diretório.
WORKDIR /app

# Etapa 3: Instalar dependências do sistema
# Instala 'curl' (para health checks) e 'build-essential' (para compilar pacotes).
# Combinar 'apt-get update', 'install' e 'clean' em uma única camada RUN reduz o tamanho da imagem.
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Etapa 4: Instalar dependências do Python
# Copiar e instalar os requirements primeiro aproveita o cache do Docker.
# Esta camada só será reconstruída se o arquivo requirements.txt mudar.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Etapa 5: Copiar o código da aplicação
# Copia o código-fonte após a instalação das dependências.
# Desta forma, alterações no código não invalidam o cache das camadas de dependências.
COPY . .

# Etapa 6: Expor a porta da aplicação
# Informa ao Docker que o contêiner escuta na porta 8000.
EXPOSE 8000

# Etapa 7: Definir o comando de inicialização
# Inicia o servidor Uvicorn.
# --host 0.0.0.0 torna o servidor acessível externamente.
# --reload é ótimo para desenvolvimento, mas deve ser removido em produção.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
