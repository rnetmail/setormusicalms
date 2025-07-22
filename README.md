# README.md
# Versão 100 22/07/2025 13:00

# 🎵 Portal do Setor Musical MS

Este é o repositório oficial da aplicação web do Setor Musical Mokiti Okada de Mato Grosso do Sul. O projeto consiste em uma API de backend desenvolvida com FastAPI e um frontend SPA (Single-Page Application) desenvolvido com React e TypeScript.

---

## 🏗️ Arquitetura da Solução

A plataforma é composta por três serviços principais, orquestrados com Docker Compose:

1.  **Frontend:** Uma aplicação em **React + TypeScript**, construída com **Vite**. Em produção, é servida por um servidor estático Node.js (`serve`). Este contêiner responde na porta `3000`.
2.  **Backend:** Uma API RESTful desenvolvida em **Python** com o framework **FastAPI**. Utiliza **SQLAlchemy** para o ORM e **Pydantic** para validação de dados, com um banco de dados **SQLite** para persistência. Este contêiner responde na porta `8000`.
3.  **Proxy Reverso (VPS):** Um servidor **Nginx** configurado na VPS (fora dos nossos contêineres) gerencia o tráfego do domínio `setormusicalms.art.br`, direcionando as requisições para os contêineres `frontend` (porta 3000) e `backend` (porta 8000).

---

## 🚀 Desenvolvimento Local

Para executar a aplicação completa em seu ambiente de desenvolvimento, siga os passos abaixo.

### Pré-requisitos
- Docker (`v20.10+`)
- Docker Compose (`v2.5+`)

### Passos para Instalação
1.  **Clone o Repositório**
    ```bash
    git clone [https://github.com/rnetmail/setormusicalms.git](https://github.com/rnetmail/setormusicalms.git)
    cd setormusicalms
    ```

2.  **Construa e Inicie os Contêineres**
    Este comando irá construir as imagens e iniciar todos os serviços.
    ```bash
    docker compose up --build -d
    ```

3.  **Inicialize o Banco de Dados (Apenas na Primeira Vez)**
    Este script cria as tabelas do banco de dados e o usuário administrador (`admin` / `Setor@MS25`).
    ```bash
    docker compose exec backend python /app/init_admin.py
    ```

4.  **Acesse a Aplicação**
    - **Frontend:** [http://localhost:3000](http://localhost:3000)
    - **Backend (Documentação da API):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testes Automatizados

A suíte de testes automatizados (Pytest + Playwright) é executada como parte do workflow de CI/CD. Para rodar localmente:

```bash
# Executar todos os testes dentro do contêiner do backend
docker compose exec backend pytest
