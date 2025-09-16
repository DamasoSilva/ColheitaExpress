# ColheitaExpress - Plataforma de E-commerce Completa

![ColheitaExpress Logo](https://via.placeholder.com/200x80/4F46E5/FFFFFF?text=ColheitaExpress)

## 📋 Sobre o Projeto

O **ColheitaExpress** é uma plataforma de e-commerce completa e robusta, desenvolvida para oferecer uma experiência de compra online excepcional. O sistema inclui funcionalidades avançadas para gestão de produtos, pedidos, entregas, pagamentos e muito mais.

### 🎯 Principais Funcionalidades

- **Sistema de Usuários Completo**: Clientes, Administradores, Funcionários e Motoristas
- **Gestão de Produtos**: CRUD completo com categorias, estoque e promoções
- **Sistema de Pedidos**: Processamento completo com rastreamento em tempo real
- **Múltiplos Métodos de Pagamento**: PIX, Cartão, Boleto, Carteira Digital
- **Sistema de Entregas**: Interface para motoristas com validação digital
- **Dashboard Administrativo**: Métricas e relatórios em tempo real
- **Sistema de Avaliações**: Reviews e comentários dos clientes
- **Notificações**: E-mail, SMS e notificações push
- **API Segura**: JWT, HTTPS, proteção CSRF/XSS
- **Sistema de Cupons**: Promoções e descontos automáticos

## 🏗️ Arquitetura do Sistema

```
ColheitaExpress/
├── backend/                 # Django REST Framework
│   ├── ecommerce_saas/     # Configurações principais
│   ├── users/              # Sistema de usuários
│   ├── products/           # Gestão de produtos
│   ├── orders/             # Sistema de pedidos
│   ├── deliveries/         # Gestão de entregas
│   ├── payments/           # Sistema de pagamentos
│   ├── coupons/            # Sistema de cupons
│   ├── notifications/      # Sistema de notificações
│   └── audit/              # Logs e auditoria
├── frontend/               # React + Vite
│   └── ecommerce-frontend/ # Interface do usuário
├── docker/                 # Configurações Docker
├── scripts/                # Scripts de deploy
└── docs/                   # Documentação
```

## 🚀 Tecnologias Utilizadas

### Backend
- **Django 5.2** - Framework web robusto
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados principal
- **Redis** - Cache e sessões
- **Celery** - Tarefas assíncronas
- **JWT** - Autenticação segura
- **Docker** - Containerização

### Frontend
- **React 19** - Interface de usuário
- **Vite** - Build tool moderno
- **Tailwind CSS** - Framework CSS
- **Radix UI** - Componentes acessíveis
- **React Router** - Roteamento
- **Recharts** - Gráficos e visualizações

### Infraestrutura
- **Docker & Docker Compose** - Containerização
- **Nginx** - Proxy reverso
- **PostgreSQL** - Banco de dados
- **Redis** - Cache e filas
- **Certbot** - Certificados SSL

## Configuração do Ambiente Local

Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

### Pré-requisitos
- Python 3.9+
- Node.js 18+
- pnpm (instalado via `npm install -g pnpm`)
- Git

### 1. Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd ecommerce-saas
```

### 2. Configurar o Back-end (Django)

Navegue até o diretório `backend`:
```bash
cd backend
```

#### 2.1. Criar e Ativar Ambiente Virtual
```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows
```

#### 2.2. Instalar Dependências
```bash
pip install -r requirements.txt
# Se o arquivo requirements.txt não existir, instale manualmente:
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt django-filter python-dotenv psycopg2-binary
```

#### 2.3. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do diretório `backend` com o seguinte conteúdo:
```
SECRET_KEY=sua_chave_secreta_aqui # Gere uma chave segura para produção
DEBUG=True
ALLOWED_HOSTS=["localhost", "127.0.0.1"]

# Configurações do Banco de Dados PostgreSQL (para produção)
# DATABASE_URL=postgres://user:password@host:port/dbname

# Configurações do Banco de Dados SQLite (para desenvolvimento)
# Por padrão, o projeto usará SQLite se DATABASE_URL não for definida
```

#### 2.4. Aplicar Migrações
```bash
python manage.py migrate
```

#### 2.5. Criar Superusuário
Para acessar o painel administrativo do Django:
```bash
python manage.py createsuperuser
```
Siga as instruções para criar um usuário. Você pode usar os dados de teste:
- **Email**: admin@ecommerce.com
- **Senha**: admin123

#### 2.6. Criar Dados de Teste (Opcional)
Para popular o banco de dados com alguns produtos, departamentos, etc.:
```bash
python manage.py shell -c "from products.models import Department, Product, Stock; d1 = Department.objects.create(name='Eletrônicos', slug='eletronicos'); d2 = Department.objects.create(name='Livros', slug='livros'); p1 = Product.objects.create(name='Smartphone X', description='Um smartphone avançado', price=1200.00, department=d1, is_active=True, is_featured=True); Stock.objects.create(product=p1, quantity=100, movement_type='in', reason='Estoque Inicial'); p2 = Product.objects.create(name='Livro de Python', description='Aprenda Python do zero', price=80.00, department=d2, is_active=True); Stock.objects.create(product=p2, quantity=50, movement_type='in', reason='Estoque Inicial'); from users.models import User; User.objects.create_user(email='cliente@ecommerce.com', password='cliente123', full_name='Cliente Teste', cpf_cnpj='111.111.111-11', phone='(11) 98765-4321', address='Rua Cliente, 123', user_type='customer'); User.objects.create_user(email='motorista@ecommerce.com', password='motorista123', full_name='Motorista Teste', cpf_cnpj='222.222.222-22', phone='(22) 91234-5678', address='Rua Motorista, 456', user_type='driver');"
```

#### 2.7. Iniciar o Servidor Back-end
```bash
python manage.py runserver
```
O back-end estará disponível em `http://127.0.0.1:8000/`.

### 3. Configurar o Front-end (React)

Abra um novo terminal e navegue até o diretório `frontend/ecommerce-frontend`:
```bash
cd ../frontend/ecommerce-frontend
```

#### 3.1. Instalar Dependências
```bash
pnpm install
```

#### 3.2. Iniciar o Servidor Front-end
```bash
pnpm run dev
```
O front-end estará disponível em `http://localhost:5173/` (ou outra porta disponível).

## Execução Local

Com ambos os servidores (back-end e front-end) rodando, você pode acessar a aplicação React no seu navegador (geralmente `http://localhost:5173/`).

- **Acesso ao Admin Django**: `http://127.0.0.1:8000/admin/`

### Usuários de Teste

- **Administrador**:
  - **Email**: admin@ecommerce.com
  - **Senha**: admin123
- **Cliente**:
  - **Email**: cliente@ecommerce.com
  - **Senha**: cliente123
- **Motorista**:
  - **Email**: motorista@ecommerce.com
  - **Senha**: motorista123

## Deploy em Hospedagem

Para fazer o deploy em um ambiente de produção, siga estas orientações:

### 1. Back-end (Django)

- **Banco de Dados**: Configure um banco de dados PostgreSQL. Atualize a variável de ambiente `DATABASE_URL` no seu `.env` com a string de conexão do PostgreSQL.
- **Variáveis de Ambiente**: Certifique-se de que `SECRET_KEY` seja uma chave forte e única. Defina `DEBUG=False` e `ALLOWED_HOSTS` com os domínios da sua aplicação em produção.
- **Servidor Web**: Use um servidor WSGI como Gunicorn ou uWSGI para servir a aplicação Django.
- **Servidor HTTP**: Use Nginx ou Apache como proxy reverso para o Gunicorn/uWSGI e para servir arquivos estáticos e de mídia.
- **Coleta de Estáticos**: Execute `python manage.py collectstatic --noinput` para coletar todos os arquivos estáticos em um único diretório que será servido pelo Nginx/Apache.
- **HTTPS**: Configure SSL/TLS para garantir a segurança das comunicações.

### 2. Front-end (React)

- **Build de Produção**: Execute `pnpm run build` no diretório `frontend/ecommerce-frontend`. Isso criará uma pasta `dist` com os arquivos estáticos otimizados.
- **Servir o Build**: Os arquivos da pasta `dist` podem ser servidos de duas maneiras:
    1.  **Integrado ao Django**: Copie o conteúdo da pasta `dist` para o diretório `static` do seu projeto Django (ex: `backend/static/`). Configure o Django para servir esses arquivos estáticos em produção (conforme o `settings.py` já preparado para isso).
    2.  **Servidor de Estáticos Separado**: Faça o deploy da pasta `dist` em um serviço de hospedagem de estáticos (como Netlify, Vercel, AWS S3 + CloudFront, etc.). Configure o front-end para apontar para a URL da sua API Django.

### Exemplo de Estrutura de Deploy (Integrado ao Django)

1.  **Build do Front-end**:
    ```bash
    cd frontend/ecommerce-frontend
    pnpm run build
    ```
2.  **Copiar para o Back-end**:
    ```bash
    cp -r dist/* ../../backend/static/
    ```
3.  **Deploy do Back-end**: O servidor Django servirá tanto a API quanto os arquivos estáticos do React.

Lembre-se de que a configuração exata pode variar dependendo do provedor de hospedagem escolhido (Heroku, AWS, Google Cloud, DigitalOcean, etc.). Sempre consulte a documentação específica do seu provedor.

## 📦 Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento)
- Python 3.11+ (para desenvolvimento)

### 🐳 Instalação com Docker (Recomendado)

1. **Clone o repositório**
```bash
git clone https://github.com/DamasoSilva/ColheitaExpress.git
cd ColheitaExpress
```

2. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

3. **Execute com Docker Compose**
```bash
docker-compose up -d
```

4. **Execute as migrações**
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

5. **Acesse a aplicação**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin: http://localhost:8000/admin

### 💻 Instalação para Desenvolvimento

#### Backend

1. **Navegue para o diretório do backend**
```bash
cd backend
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Execute o servidor**
```bash
python manage.py runserver
```

#### Frontend

1. **Navegue para o diretório do frontend**
```bash
cd frontend/ecommerce-frontend
```

2. **Instale as dependências**
```bash
pnpm install
# ou
npm install
```

3. **Execute o servidor de desenvolvimento**
```bash
pnpm dev
# ou
npm run dev
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Django
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.com

# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/colheitaexpress

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app

# Pagamentos
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Frontend
FRONTEND_URL=http://localhost:3000
```

## 🔐 Segurança

O sistema implementa várias camadas de segurança:

- **Autenticação JWT** com refresh tokens
- **Proteção CSRF/XSS**
- **Rate Limiting** para APIs
- **Validação de entrada** rigorosa
- **Logs de auditoria** completos
- **Criptografia de senhas** com bcrypt
- **HTTPS** obrigatório em produção

## 📊 Monitoramento

### Logs

Os logs são organizados em diferentes níveis:

- **INFO**: Operações normais
- **WARNING**: Situações que requerem atenção
- **ERROR**: Erros que precisam ser corrigidos
- **DEBUG**: Informações detalhadas para desenvolvimento

### Métricas

O dashboard administrativo inclui:

- Total de usuários, pedidos e produtos
- Vendas por período
- Produtos mais vendidos
- Performance de entregas
- Métricas de pagamento

## 🧪 Testes

### Backend

```bash
cd backend
python manage.py test
```

### Frontend

```bash
cd frontend/ecommerce-frontend
pnpm test
```

### Testes E2E

```bash
pnpm test:e2e
```

## 🚀 Deploy em Produção

### Deploy com Docker

1. **Configure o ambiente de produção**
```bash
cp .env.example .env.production
# Configure as variáveis para produção
```

2. **Execute o deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Deploy Manual

Consulte o arquivo `docs/DEPLOY.md` para instruções detalhadas de deploy manual.

## 📚 Documentação

- [Guia de Instalação](docs/INSTALLATION.md)
- [Guia de Deploy](docs/DEPLOY.md)
- [Documentação da API](docs/API.md)
- [Guia de Contribuição](docs/CONTRIBUTING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Equipe

- **Desenvolvedor Principal**: [Damaso Silva](https://github.com/DamasoSilva)

## 📞 Suporte

Para suporte técnico ou dúvidas:

- 📧 Email: suporte@colheitaexpress.com
- 💬 Discord: [Link do Discord]
- 📱 WhatsApp: +55 (11) 99999-9999

## 🔄 Changelog

### v1.0.0 (2024-09-16)
- ✨ Lançamento inicial
- 🔐 Sistema de autenticação completo
- 🛒 Sistema de e-commerce funcional
- 📱 Interface responsiva
- 🚚 Sistema de entregas
- 💳 Múltiplos métodos de pagamento

---

**ColheitaExpress** - Sua plataforma de e-commerce completa e robusta! 🚀

