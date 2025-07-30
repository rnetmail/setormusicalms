# fastapi_backend/Dockerfile
# Versão 10 - 29/07/2025 05:25 - Define o PYTHONPATH e o comando de inicialização correto

# Usa uma imagem base do Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Define a variável de ambiente PYTHONPATH para incluir o diretório de trabalho
# Isso resolve problemas de importação, permitindo que módulos como 'auth' e 'crud' sejam encontrados
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia todo o código do backend para o diretório de trabalho
COPY . .

# Expõe a porta 8000, que é a porta que o Uvicorn usará
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn
# Ele aponta para a variável 'app' dentro do arquivo 'app/main.py'
# --host 0.0.0.0 permite que o servidor seja acessível de fora do contêiner
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
