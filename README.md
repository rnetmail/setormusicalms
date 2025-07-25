# README.md
# Versão 102 24/07/2025 16:54

# 🎵 Portal do Setor Musical MS

Este é o repositório oficial da aplicação web do Setor Musical Mokiti Okada de Mato Grosso do Sul. O projeto consiste em uma API de backend desenvolvida com FastAPI e um frontend SPA (Single-Page Application) desenvolvido com React e TypeScript.

---

## 🏗️ Arquitetura da Solução

A plataforma é composta por três serviços principais, orquestrados com Docker Compose:

1.  **Frontend:** Uma aplicação em **React + TypeScript**, construída com **Vite**. Em produção, é servida por um servidor estático Node.js (`serve`). Este contêiner responde internamente na porta `3000`.
2.  **Backend:** Uma API RESTful desenvolvida em **Python** com o framework **FastAPI**. Utiliza **SQLAlchemy** para o ORM e **Pantic** para validação de dados, com um banco de dados **SQLite** para persistência. Este contêiner responde internamente na porta `8000`.
3.  **Proxy Reverso (VPS):** Um servidor **Nginx** configurado na VPS (fora dos nossos contêineres) gerencia o tráfego do domínio `setormusicalms.art.br` (portas 80/443), direcionando as requisições para os contêineres `frontend` (na porta `3000` da VPS) e `backend` (na porta `8000` da VPS).

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
    ```bash
    docker compose up --build -d
    ```

3.  **Inicialize o Banco de Dados (Apenas na Primeira Vez)**
    ```bash
    docker compose exec backend python /app/init_admin.py
    ```

4.  **Acesse a Aplicação**
    Após os passos anteriores, a aplicação estará disponível localmente nos seguintes endereços:
    -   **Frontend:** [http://localhost:3000](http://localhost:3000) (Esta é a porta mapeada no `docker-compose.yml` para o contêiner do frontend).
    -   **Backend (Documentação da API):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testes Automatizados

Os testes são executados automaticamente no workflow de CI/CD. Para rodar localmente:

```bash
# Executar todos os testes dentro do contêiner do backend
docker compose exec backend pytest
