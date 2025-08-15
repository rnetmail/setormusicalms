# Setor Musical Mokiti Okada MS

Sistema de gestão para o Setor Musical Mokiti Okada MS, desenvolvido com FastAPI (backend) e React (frontend).

## Tecnologias Utilizadas

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: React 18 + TailwindCSS
- **Banco de Dados**: PostgreSQL
- **Deploy**: Docker + GitHub Actions

## Estrutura do Projeto

```
setormusicalms-main/
├── fastapi_backend/      # API REST em FastAPI
├── frontend/             # Interface web em React
├── .github/workflows/    # Configurações de CI/CD
├── docker-compose.yml    # Configuração de containers
└── nginx-proxy.conf      # Configuração do proxy reverso
```

## Configuração do Banco de Dados

O sistema utiliza **exclusivamente** PostgreSQL como banco de dados. Esta configuração garante:

- **Alta disponibilidade**: Gerenciamento adequado de conexões múltiplas
- **Integridade de dados**: Suporte completo a transações ACID
- **Persistência de dados**: Volume Docker dedicado para preservação dos dados
- **Escalabilidade**: Preparado para crescimento do acervo musical

### Persistência de Dados

A persistência de dados é garantida através de volumes Docker:

```yaml
volumes:
  postgres_data:
    driver: local
```

Este volume mapeia o diretório de dados do PostgreSQL dentro do container para o sistema host, garantindo que os dados sejam preservados mesmo quando os containers são atualizados ou recriados.

## Instalação e Execução

### Requisitos

- Docker e Docker Compose
- Git

### Passos para Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/setormusicalms.git
   cd setormusicalms
   ```

2. Configure o ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env conforme necessário
   ```

3. Inicie os serviços:
   ```bash
   docker-compose up -d
   ```

4. Acesse a aplicação:
   - Frontend: http://localhost:8001
   - API: http://localhost:8001/api/

## Deploy em Produção

O sistema está configurado para deploy automático via GitHub Actions quando há push na branch principal. As etapas incluem:

1. Construção e teste das imagens Docker
2. Push das imagens para o GitHub Container Registry
3. Deploy automático no servidor de produção

### Garantindo a Segurança dos Dados em Produção

Para garantir a segurança e persistência dos dados em produção:

1. Configure backups regulares do volume PostgreSQL:
   ```bash
   # Exemplo de backup diário
   docker exec setormusicalms-db pg_dump -U mestre setormusicalms_db > backup_$(date +%Y%m%d).sql
   ```

2. Antes de qualquer atualização de produção, crie um backup extra:
   ```bash
   # No servidor de produção
   docker exec setormusicalms-db pg_dump -U mestre setormusicalms_db > backup_pre_deploy.sql
   ```

3. O volume de dados do PostgreSQL deve ser mantido mesmo durante atualizações:
   ```bash
   # Exemplo de atualização segura
   docker-compose pull
   docker-compose down backend frontend nginx-proxy
   docker-compose up -d
   ```

## Administração

O sistema possui uma área de administração acessível via frontend, onde é possível:

1. Gerenciar o repertório
2. Administrar eventos na agenda
3. Publicar recados e notícias
4. Gerenciar usuários
5. Publicar fotos e vídeos na galeria

## Desenvolvimento

Para desenvolvimento local, siga as instruções de instalação acima e utilize os comandos específicos para desenvolvimento.

## Licença

Este projeto é proprietário e seu uso é restrito ao Setor Musical Mokiti Okada MS.