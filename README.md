# README.md
# Versão 114 - Documentação Final e Definitiva

# 🎵 Portal do Setor Musical MS

Este é o repositório oficial da aplicação web do Setor Musical Mokiti Okada de Mato Grosso do Sul. O projeto consiste em uma API de backend desenvolvida com FastAPI e um frontend SPA (Single-Page Application) desenvolvido com React e TypeScript, totalmente containerizado com Docker.

---

## 🏗️ Arquitetura da Solução

A arquitetura foi projetada para ser robusta, escalável e independente do ambiente do servidor.

1.  **Backend (`backend`):**
    * **Tecnologia:** API RESTful em Python com **FastAPI**.
    * **Banco de Dados:** **SQLite**, persistido através de um volume Docker para simplicidade e portabilidade.
    * **Servidor:** `uvicorn` rodando internamente na porta **8000**.
    * **Comunicação:** Não expõe portas diretamente para o host, comunicando-se apenas através da rede interna do Docker com o `nginx-proxy`.

2.  **Frontend (`frontend`):**
    * **Tecnologia:** SPA em **React + TypeScript**, construída com **Vite**.
    * **Servidor:** Servidor estático Node.js (`serve`) rodando internamente na porta **3000**.
    * **Comunicação:** Não expõe portas diretamente para o host, sendo acessível apenas através do `nginx-proxy`.

3.  **Proxy Interno (`nginx-proxy`):**
    * **Tecnologia:** Contêiner **Nginx** que atua como o **ponto de entrada único** para a aplicação.
    * **Função:** Recebe todo o tráfego na porta **8001** da VPS e o roteia para os serviços corretos dentro da rede Docker:
        * Requisições para a raiz (`/`) são encaminhadas para o `frontend` na porta 3000.
        * Requisições para a API (`/api/`) são encaminhadas para o `backend` na porta 8000.
    * **Vantagem:** Esta abordagem encapsula toda a lógica de roteamento da aplicação, tornando-a independente da configuração do Nginx da VPS.

4.  **Proxy Externo (Nginx da VPS):**
    * Este servidor, gerenciado pelo provedor de hospedagem, tem uma única e simples responsabilidade: encaminhar todo o tráfego do domínio `setormusicalms.art.br` (portas 80/443) para a porta `8001` da VPS, onde nosso `nginx-proxy` está ouvindo.

---

## 🚀 Desenvolvimento Local

1.  **Clone o Repositório:** `git clone https://github.com/rnetmail/setormusicalms.git && cd setormusicalms`
2.  **Inicie os Contêineres:** `docker compose up --build -d`
3.  **Inicialize o Banco de Dados (Primeira vez):** `docker compose exec backend python /app/init_admin.py`
4.  **Acesse a Aplicação:**
    * **Frontend:** [http://localhost:8001](http://localhost:8001)
    * **Backend (Documentação):** [http://localhost:8000/docs](http://localhost:8000/docs) (Acessível apenas via `localhost`, pois não está exposto pelo proxy).

---

## 🔄 Deploy (CI/CD) com GitHub Actions

O deploy é automatizado via GitHub Actions (`.github/workflows/deploy.yml`) e acionado a cada `push` na branch `main`.

### Etapas do Workflow

1.  **Build & Push (`build_and_push`):**
    * Conecta-se ao GitHub Container Registry (ghcr.io).
    * Constrói as imagens Docker de produção para o `frontend` e o `backend`.
    * Envia as novas imagens para o `ghcr.io` com a tag `:latest`.

2.  **Deploy & Validação (`deploy_and_validate`):**
    * **Conexão:** Acessa a VPS de produção via SSH usando uma chave privada.
    * **Autenticação:** Configura a autenticação do Docker na VPS para acessar o `ghcr.io`.
    * **Atualização:** Executa a sequência `docker compose down`, `docker compose pull` e `docker compose up -d` para parar os contêineres antigos, baixar as novas imagens e iniciar a nova versão da aplicação.
    * **Validação:** Após um tempo de espera, o workflow valida se a aplicação está funcional, acessando o endpoint `http://setormusicalms.art.br/api/health`. Em caso de falha, exibe os logs do contêiner do backend para facilitar o diagnóstico.

### 🤫 Segredos do Repositório (Secrets)

Para que o deploy funcione, os seguintes segredos devem ser configurados no ambiente de `prod` do repositório em **Settings > Environments > prod**.

| Segredo                  | Descrição                                                                                                  | Como Obter / Exemplo                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `VPS_HOST`               | Endereço IP do servidor VPS para o deploy.                                                                 | `194.195.221.198`                                                                                                  |
| `VPS_SSH_USER`           | Nome de usuário para a conexão SSH com a VPS.                                                              | `setormusicalms`                                                                                                   |
| `VPS_SSH_PRIVATE_KEY`    | A **chave SSH privada** (não a pública) para autenticação sem senha na VPS.                                | Copie o conteúdo do seu arquivo de chave privada, geralmente `~/.ssh/id_rsa`.                                        |
| `PROJECT_PATH_ON_VPS`    | O caminho absoluto para a pasta do projeto na VPS onde o `docker-compose.yml` está localizado.             | `/home/setormusicalms/setormusical/setormusicalms`                                                                   |
| `DOCKER_CONFIG_JSON`     | Credencial de autenticação do Docker em formato JSON para o `ghcr.io`.                                     | Execute `docker login ghcr.io` na sua máquina local e copie o conteúdo do arquivo `~/.docker/config.json`.         |

---

### ⚙️ Configuração Essencial da VPS

Para que a automação funcione, a VPS precisa de uma única configuração de permissão:

**Adicionar Usuário ao Grupo Docker:** O usuário do deploy (`setormusicalms`) precisa pertencer ao grupo `docker` para poder gerenciar os contêineres sem precisar de senha `sudo`.

Execute os seguintes comandos na VPS:
```bash
# Adiciona o usuário ao grupo docker
sudo usermod -aG docker setormusicalms

# Reinicia a VPS para garantir que as permissões sejam aplicadas
sudo reboot
