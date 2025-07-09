# 🎵 Setor Musical Mokiti Okada MS

Sistema de gestão digital para o Coral e Orquestra de Violões Mokiti Okada de Mato Grosso do Sul.

## 🌐 Acesso

- **Site Principal**: [setormusicalms.art.br](https://setormusicalms.art.br)
- **Painel de Gestão**: [setormusicalms.art.br/#/gestao/login](https://setormusicalms.art.br/#/gestao/login)

## 📋 Sobre o Projeto

Este sistema foi desenvolvido para centralizar e facilitar o acesso aos materiais de estudo, agenda de atividades e informações do Setor Musical. Os usuários podem:

- 🎼 **Acessar repertórios** com partituras, áudios e vídeos
- 📅 **Consultar agenda** de ensaios e apresentações  
- 📢 **Ler recados** importantes
- 📖 **Conhecer a história** do setor
- 🖼️ **Ver galeria** de fotos e momentos

## 🛠️ Tecnologias

### Frontend
- **React 18** com TypeScript
- **Vite** para build e desenvolvimento
- **Tailwind CSS** para estilização
- **React Router** para navegação

### Backend
- **Django 4.2** com Python 3.11
- **Django REST Framework** para APIs
- **PostgreSQL 14** como banco de dados
- **Token Authentication** para segurança

### Infraestrutura
- **Docker** e **Docker Compose**
- **Nginx** para proxy reverso
- **GitHub Actions** para CI/CD
- **VPS** com deploy automatizado

## 🚀 Deploy Automático

O projeto possui workflow completo de CI/CD configurado no GitHub Actions.

### Como fazer deploy:

1. Faça suas alterações no código
2. Commit com mensagem contendo **"Deploy to VPS"**:
   ```bash
   git commit -m "Deploy to VPS - Suas alterações aqui"
   git push origin main
   ```
3. O workflow será executado automaticamente
4. Aguarde a conclusão (≈ 5-10 minutos)
5. Verifique o site em produção

### Workflow inclui:
- ✅ Build do frontend
- ✅ Validação do backend  
- ✅ Testes automatizados
- ✅ Deploy na VPS
- ✅ Health checks
- ✅ Logs detalhados

## 🔧 Desenvolvimento Local

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- Docker e Docker Compose
- Git

### Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/rnetmail/setormusicalms.git
   cd setormusicalms
   ```

2. **Configure variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

3. **Inicie com Docker**:
   ```bash
   docker-compose up -d
   ```

4. **Acesse localmente**:
   - Frontend: http://localhost:8001
   - Backend API: http://localhost:8001/api/

### Desenvolvimento Frontend

```bash
# Instalar dependências
npm install

# Servidor de desenvolvimento
npm run dev

# Build para produção
npm run build
```

### Desenvolvimento Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Servidor de desenvolvimento
python manage.py runserver
```

## 📱 Funcionalidades

### Para Usuários Públicos
- Visualização de repertórios (Coral e Orquestra)
- Acesso a partituras, áudios e vídeos
- Consulta de agenda de atividades
- Leitura de recados e história

### Para Administradores
- CRUD completo de repertórios
- Gestão de agenda e eventos
- Publicação de recados
- Gerenciamento de usuários
- Upload e organização de mídias

## 🎵 Reprodução de Mídias

O sistema suporta mídias hospedadas no Google Drive:

### Configuração de URLs

**Para áudio/vídeo (reprodução direta)**:
```
https://drive.google.com/uc?export=download&id=SEU_FILE_ID
```

**Para PDF/preview**:
```
https://drive.google.com/file/d/SEU_FILE_ID/preview
```

### Permissões Necessárias
- Arquivo deve estar com permissão: **"Qualquer pessoa com o link pode visualizar"**
- Não pode estar restrito a usuários específicos

### Formatos Suportados
- **Áudio**: MP3 (recomendado)
- **Vídeo**: MP4, YouTube embeds
- **Partituras**: PDF, imagens (JPG, PNG)

## 🔐 Autenticação

### Acesso Administrativo
- **URL**: https://setormusicalms.art.br/#/gestao/login
- **Usuário padrão**: admin
- **Senha padrão**: Setor@MS25

### Sistema de Permissões
- Usuários autenticados: Acesso total ao painel
- Usuários públicos: Apenas visualização
- Token-based authentication via Django REST Framework

## 📊 Monitoramento

### Health Checks
O sistema possui health checks automáticos para:
- ✅ Frontend (Nginx)
- ✅ Backend (Django)
- ✅ Banco de dados (PostgreSQL)

### Logs
- Logs estruturados em JSON
- Rotação automática
- Níveis: INFO, WARNING, ERROR

## 🛡️ Segurança

### Configurações de Produção
- DEBUG=False em produção
- HTTPS obrigatório
- CORS configurado
- Headers de segurança
- Validação de entrada

### Backup
- Backup automático do banco de dados
- Versionamento de código no Git
- Volumes Docker persistentes

## 📚 Estrutura do Projeto

```
setormusicalms/
├── .github/workflows/     # GitHub Actions
├── backend/              # Django API
│   ├── api/             # App principal
│   ├── backend/         # Configurações
│   └── requirements.txt
├── src/                 # Frontend React
├── public/              # Assets estáticos
├── docker-compose.yml   # Orquestração
├── Dockerfile          # Frontend container
└── nginx.conf          # Configuração Nginx
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno do Setor Musical Mokiti Okada MS.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Entre em contato com a equipe técnica
- Consulte a documentação técnica

---

**Desenvolvido com ❤️ para o Setor Musical Mokiti Okada MS**

# Deploy forçado Tue Jul  8 22:55:34 EDT 2025
