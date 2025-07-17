# fastapi_backend/README.md
# Versão 81 18/07/2025 09:42

# Setor Musical MS - API e Frontend

Este projeto contém uma aplicação web completa com um backend FastAPI e um frontend React.

## Visão Geral da Arquitetura

- **Backend:** Uma API RESTful construída com **FastAPI**, servindo dados a partir de um banco de dados **SQLite**.
- **Frontend:** Uma Single-Page Application (SPA) construída com **React** e **TypeScript**.
- **Containerização:** A aplicação inteira é containerizada usando **Docker** e orquestrada com **Docker Compose**.
- **Servidor Web:** O **Nginx** é usado como servidor web para o frontend React e como proxy reverso para a API FastAPI.

## Estrutura de Pastas

- `fastapi_backend/`: Contém todo o código-fonte da API FastAPI.
  - `app/`: Onde a aplicação FastAPI e os seus routers são definidos.
  - `models/`: Contém os modelos de dados do SQLAlchemy.
  - `schemas/`: Contém os schemas de validação de dados do Pydantic.
  - `crud/`: Contém a lógica de acesso ao banco de dados (Create, Read, Update, Delete).
- `src/` (ou raiz): Contém o código-fonte do frontend React.
- `docker-compose.yml`: Define os serviços, redes e volumes do Docker.
- `Dockerfile`: Usado para construir a imagem do frontend.
- `fastapi_backend/Dockerfile`: Usado para construir a imagem do backend.

## Rodando Localmente

**Pré-requisitos:**
- Docker
- Docker Compose v2

**Passos:**

1.  **Construir e Iniciar os Contentores:**
    Na raiz do projeto, execute:
    ```bash
    docker compose up --build -d
    ```

2.  **Inicializar o Banco de Dados (Apenas na primeira vez):**
    Para criar as tabelas e o usuário administrador padrão, execute:
    ```bash
    docker compose exec backend python init_admin.py
    ```

3.  **Aceder à Aplicação:**
    - **Frontend:** [http://localhost:3000](http://localhost:3000)
    - **Backend (API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Rodando os Testes

Para executar a suíte de testes automatizados, use o seguinte comando:
```bash
docker compose exec backend pytest
