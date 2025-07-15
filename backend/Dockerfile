# setormusicalms/backend/Dockerfile

# Estágio 1: Builder - Instala dependências em um ambiente isolado
FROM python:3.11-slim as builder

WORKDIR /app

# Cria um ambiente virtual para isolar as dependências
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências no ambiente virtual
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Estágio 2: Runtime - Configura a imagem final e mais leve
FROM python:3.11-slim

WORKDIR /app

# Copia o ambiente virtual com as dependências já instaladas do estágio de build
COPY --from=builder /opt/venv /opt/venv

# Cria um usuário não-root para rodar a aplicação por segurança
RUN useradd --create-home appuser
USER appuser

# Copia o código da aplicação
COPY ./app ./app

# Define o PATH para incluir o venv e expõe a porta
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

