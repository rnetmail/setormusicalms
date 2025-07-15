# Setor Musical MS

Este é o repositório para o sistema de gerenciamento do Setor Musical MS. A aplicação foi desenvolvida utilizando uma arquitetura moderna e containerizada para facilitar o desenvolvimento e o deploy.

## 🚀 Arquitetura 

O projeto é composto por dois serviços principais, orquestrados com Docker Compose:

*   **Backend:** Uma API RESTful desenvolvida com **FastAPI** (Python).
*   **Frontend:** Uma aplicação single-page (SPA) (assumindo React/Vue/Angular).
*   **Banco de Dados:** **SQLite**, persistido através de um volume Docker para simplicidade e portabilidade.
*   **CI/CD:** O deploy é automatizado via **GitHub Actions**. A cada push na branch `main`, os testes são executados e, se passarem, a nova versão é enviada para a VPS, onde a aplicação é reiniciada.

## 📋 Pré-requisitos

*   Docker
*   Docker Compose

## 💻 Rodando Localmente

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/setormusicalms.git
    cd setormusicalms
    ```

2.  **Suba os containers:**
    O comando a seguir irá construir as imagens do frontend e backend e iniciar os containers.
    ```bash
    docker-compose up --build
    ```

3.  **Acesse as aplicações:**
    *   **Frontend:** http://localhost:3000
    *   **Backend (API Docs):** http://localhost:8000/docs

O banco de dados SQLite será criado e armazenado no volume `sqlite_db` gerenciado pelo Docker.

## 🧪 Rodando os Testes

Para executar os testes do backend manualmente:

```bash
docker-compose exec backend pytest
```

## ⚙️ Deploy

O deploy para o ambiente de produção (VPS) é totalmente automatizado. Simplesmente faça um push ou merge para a branch `main`. O workflow do GitHub Actions (`.github/workflows/deploy.yml`) se encarregará de:

1.  Rodar os testes para garantir a integridade do código.
2.  Sincronizar os arquivos do projeto com o servidor via `rsync`.
3.  Reiniciar os serviços no servidor usando `docker-compose` para que as novas alterações entrem no ar.

