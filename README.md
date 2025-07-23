# README.md
# Versão 104 22/07/2025 23:25

# 🎵 Portal do Setor Musical MS

Este é o repositório oficial da aplicação web do Setor Musical Mokiti Okada de Mato Grosso do Sul. O projeto consiste em uma API de backend desenvolvida com FastAPI e um frontend SPA (Single-Page Application) desenvolvido com React e TypeScript, totalmente orquestrado com Docker.

---

## 🏗️ Arquitetura e Fluxo de Rede

A plataforma foi desenhada para ser robusta e escalável, utilizando contêineres para separar as responsabilidades. O fluxo de uma requisição do utilizador até a aplicação é o seguinte:

1.  **Nginx da VPS (Externo):** O utilizador acede `setormusicalms.art.br`. O Nginx principal da VPS, que ouve nas portas 80/443, atua como um proxy reverso e encaminha todo o tráfego para `http://127.0.0.1:8001`.
2.  **Nginx do Projeto (Interno):** Um contêiner Nginx dedicado ao projeto recebe as requisições na porta `8001`. Este Nginx é o maestro da aplicação, responsável por:
    * **Servir o Frontend:** Se a requisição for para a aplicação React (ex: `/`, `/coral/repertorio`), ele entrega os ficheiros estáticos (HTML, CSS, JS).
    * **Redirecionar para a API:** Se a requisição for para a API (ex: `/api/repertorio`), ele a redireciona para o contêiner do backend na porta `8000`.
3.  **Backend (FastAPI):** O contêiner do backend ouve na porta `8000` e processa a lógica de negócio, interagindo com o banco de dados.
4.  **Banco de Dados (SQLite):** Um volume Docker garante que os dados do SQLite sejam persistidos entre reinicializações dos contêineres.

```mermaid
graph TD
    A[Utilizador via setormusicalms.art.br] --> B{Nginx na VPS (Porta 80/443)};
    B --> C[Host da VPS];
    subgraph Docker
        C -- Porta 8001 --> D{Nginx do Projeto};
        D -- /api/* --> E[Backend FastAPI :8000];
        D -- /* --> F[Ficheiros React];
        E <--> G[(Banco de Dados SQLite)];
    end
🛠️ Stack Tecnológica
Camada	Tecnologia	Descrição
Frontend	React, TypeScript, Vite	Interface de utilizador reativa e moderna.
Tailwind CSS	Framework de estilização para um design rápido e consistente.
Backend	Python, FastAPI	API de alta performance e fácil desenvolvimento.
SQLAlchemy	ORM para interação com o banco de dados.
Pydantic	Validação de dados robusta para as requisições da API.
Banco de Dados	SQLite	Banco de dados relacional leve e baseado em ficheiro.
Orquestração	Docker, Docker Compose	Containerização e gestão dos serviços da aplicação.
Servidor/Proxy	Nginx	Servidor web para o frontend e proxy reverso para o backend.
CI/CD	GitHub Actions	Automação de testes e deploy contínuo.

Exportar para as Planilhas
🚀 Desenvolvimento Local
Siga estes passos para executar a aplicação completa no seu ambiente local.

Pré-requisitos
Docker (v20.10+)

Docker Compose (v2.5+)

Passos para Instalação
Clone o Repositório

Bash

git clone [https://github.com/rnetmail/setormusicalms.git](https://github.com/rnetmail/setormusicalms.git)
cd setormusicalms
Crie o Ficheiro de Ambiente
Copie o ficheiro de exemplo .env.example para .env. Para a configuração padrão de desenvolvimento local, nenhuma alteração é necessária.

Bash

cp .env.example .env
Construa e Inicie os Contêineres
Este comando irá construir as imagens e iniciar todos os serviços em segundo plano.

Bash

docker compose up --build -d
Inicialize o Banco de Dados (Apenas na Primeira Vez)
Este script cria as tabelas do SQLite e o utilizador administrador (admin / Setor@MS25).

Bash

docker compose exec backend python /app/init_admin.py
Acesse a Aplicação

Frontend: http://localhost:8001

Backend (Documentação da API): http://localhost:8000/docs

Comandos Úteis do Docker
Parar todos os serviços: docker compose down

Ver logs em tempo real: docker compose logs -f

Aceder a um shell no backend: docker compose exec backend bash

⚙️ Configurações
Variáveis de Ambiente
As configurações da aplicação são geridas através de variáveis de ambiente definidas no ficheiro .env na raiz do projeto. O ficheiro .env.example serve como um template.

DATABASE_URL: A URL de conexão para o banco de dados. O padrão é sqlite:///data/setormusical.db.

SECRET_KEY: Chave secreta para a assinatura de tokens JWT.

ADMIN_USER/ADMIN_PASS: Credenciais para o utilizador administrador inicial.

Configuração do Nginx Interno (nginx.conf)
O ficheiro nginx.conf na raiz do projeto é responsável por rotear o tráfego que chega na porta 8001.

Nginx

# nginx.conf
server {
    listen 80; # Ouve na porta 80 DENTRO da rede Docker

    # Serve os ficheiros do frontend
    location / {
        root   /usr/share/nginx/html;
        index  index.html;
        try_files $uri $uri/ /index.html; # Essencial para React Router
    }

    # Redireciona os pedidos de API para o serviço de backend
    location /api/ {
        # 'backend' é o nome do serviço no docker-compose.yml
        proxy_pass http://backend:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
🧪 Testes Automatizados
A suíte de testes utiliza Pytest para validar a API e Playwright para testes de ponta a ponta (E2E) na interface do utilizador.

Para rodar os testes localmente:

Bash

# Certifique-se de que os contêineres estão em execução
docker compose up -d

# Execute todos os testes dentro do contêiner do backend
docker compose exec backend pytest
🔄 CI/CD - Integração e Deploy Contínuos
O projeto utiliza GitHub Actions para automatizar os processos de teste e deploy. O workflow está definido em .github/workflows/deploy.yml.

O pipeline executa os seguintes passos a cada push na branch main:

Testar: Constrói o ambiente Docker, inicia os serviços e executa a suíte de testes completa.

Construir e Publicar: Se os testes passarem, constrói as imagens Docker do backend e do nginx e as publica no GitHub Container Registry (ghcr.io).

Deploy: Conecta-se à VPS via SSH, faz o pull das novas imagens do registry e reinicia os serviços com docker compose.

Validar: Após o deploy, verifica se os endpoints do frontend e do backend estão online e a responder corretamente.
