# README.md
# Versão 22 18/07/2025 00:15

# 🎵 Setor Musical MS - API e Frontend

Este é o repositório oficial da aplicação web do Setor Musical Mokiti Okada de Mato Grosso do Sul. O projeto consiste em uma API de backend desenvolvida com FastAPI e um frontend SPA (Single-Page Application) desenvolvido com React e TypeScript.

## 🏗️ Visão Geral da Arquitetura

-   **Backend:** Uma API RESTful moderna construída com **FastAPI**, utilizando SQLAlchemy para o ORM e Pydantic para validação de dados. Para desenvolvimento local, utiliza um banco de dados **SQLite**.
-   **Frontend:** Uma aplicação interativa construída com **React**, **TypeScript** e **Vite**, estilizada com **Tailwind CSS**.
-   **Containerização:** A aplicação inteira é containerizada usando **Docker** e orquestrada com **Docker Compose** para simplificar a configuração do ambiente de desenvolvimento.
-   **Servidor Web:** **Nginx** é utilizado em produção (e no build Docker) para servir os arquivos estáticos do frontend e atuar como proxy reverso para a API do backend.

## 🚀 Rodando o Projeto Localmente

Siga os passos abaixo para executar a aplicação completa em seu ambiente de desenvolvimento.

### Pré-requisitos

-   Docker (`v20.10+`)
-   Docker Compose (`v2.5+`)

### Passos para Instalação

1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/rnetmail/setormusicalms.git](https://github.com/rnetmail/setormusicalms.git)
    cd setormusicalms
    ```

2.  **Construa e Inicie os Contentores**
    Este comando irá construir as imagens do frontend e do backend e iniciar todos os serviços definidos no `docker-compose.yml`.
    ```bash
    docker compose up --build -d
    ```

3.  **Inicialize o Banco de Dados (Apenas na Primeira Vez)**
    Este script cria as tabelas do banco de dados SQLite e insere o usuário administrador padrão (`admin` / `Setor@MS25`).
    ```bash
    docker compose exec backend python init_admin.py
    ```

4.  **Aceda à Aplicação**
    Após os passos anteriores, a aplicação estará disponível nos seguintes endereços:
    -   **Frontend:** [http://localhost:3000](http://localhost:3000)
    -   **Backend (Documentação da API):** [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Executando os Testes

A suíte de testes automatizados utiliza `pytest` para testes de API e `Playwright` para testes de interface. Para executá-los, o ambiente Docker deve estar de pé.

```bash
# Executar todos os testes dentro do contentor do backend
docker compose exec backend pytest
