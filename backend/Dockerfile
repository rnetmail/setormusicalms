# backend/Dockerfile

FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . /app/

# Criar diretórios para arquivos estáticos e mídia
RUN mkdir -p /app/static /app/media

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."

# Criar script de entrada
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Aguardando banco de dados..."\n\
while ! pg_isready -h $SQL_HOST -p $SQL_PORT -U $POSTGRES_USER; do\n\
  echo "Banco de dados não está pronto - aguardando..."\n\
  sleep 2\n\
done\n\
echo "Banco de dados está pronto!"\n\
\n\
echo "Executando migrações..."\n\
python manage.py migrate --noinput\n\
\n\
echo "Criando superusuário se não existir..."\n\
python manage.py shell << EOF\n\
from django.contrib.auth.models import User\n\
import os\n\
\n\
username = os.environ.get("ADMIN_USER", "admin")\n\
password = os.environ.get("ADMIN_PASS", "Setor@MS25")\n\
email = "admin@setormusicalms.art.br"\n\
\n\
if not User.objects.filter(username=username).exists():\n\
    User.objects.create_superuser(username, email, password)\n\
    print(f"Superusuário {username} criado com sucesso!")\n\
else:\n\
    print(f"Superusuário {username} já existe.")\n\
EOF\n\
\n\
echo "Coletando arquivos estáticos..."\n\
python manage.py collectstatic --noinput\n\
\n\
echo "Iniciando servidor..."\n\
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3\n\
' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/ || exit 1

# Comando de entrada
ENTRYPOINT ["/app/entrypoint.sh"]

