# E-commerce SaaS - Plataforma Completa

Este projeto é uma plataforma de e-commerce SaaS (Software as a Service) robusta e completa, desenvolvida com Python (Django/Django REST Framework) para o back-end e React para o front-end. Ele oferece interfaces diferenciadas para Administradores, Clientes e Motoristas, gestão de produtos, controle de estoque, sistema de pedidos e acompanhamento de entregas.

## Funcionalidades Principais

### Geral
- **Arquitetura SaaS**: Projetado para ser escalável e multi-tenant (embora a implementação multi-tenant completa exija mais detalhes, a estrutura base está pronta).
- **Responsividade**: Interface de usuário adaptável a diferentes tamanhos de tela (desktops, tablets, celulares).
- **Segurança**: Sistema de autenticação e autorização robusto.

### Back-end (Django/Django REST Framework)
- **Gestão de Usuários**: Cadastro e gerenciamento de Administradores, Clientes e Motoristas.
  - **Administrador**: Acesso total ao sistema, gestão de produtos, pedidos, entregas, usuários.
  - **Cliente**: Visualização de produtos, realização de pedidos, acompanhamento de entregas, gestão de perfil.
  - **Motorista**: Acesso a entregas atribuídas, detalhes do pedido e endereço de entrega.
- **Gestão de Produtos**: Cadastro, edição e listagem de produtos.
  - **Departamentos**: Categorização de produtos.
  - **Controle de Estoque**: Sistema completo de movimentações de entrada, saída e ajustes.
- **Sistema de Pedidos**: Criação, visualização, atualização de status e cancelamento de pedidos.
- **Sistema de Entregas**: Atribuição de entregas a motoristas, rastreamento de status e acompanhamento pelo cliente.
- **Banco de Dados Relacional**: Suporte a PostgreSQL (recomendado para produção) e SQLite (para desenvolvimento).
- **API RESTful**: Endpoints bem definidos para todas as funcionalidades, facilitando a integração com o front-end e outras aplicações.

### Front-end (React)
- **Interfaces Diferenciadas**: Dashboards específicos para Administrador, Cliente e Motorista.
- **Página Inicial (Landing Page)**: Design moderno e responsivo para apresentar o e-commerce.
- **E-commerce Completo**: 
  - **Catálogo de Produtos**: Listagem com filtros, busca e ordenação
  - **Detalhes do Produto**: Página completa com especificações, avaliações e galeria de imagens
  - **Carrinho de Compras**: Gestão de itens, quantidades e cupons de desconto
  - **Checkout**: Processo completo de finalização com dados pessoais, endereço e pagamento
  - **Confirmação de Pedido**: Página de sucesso com detalhes e acompanhamento
- **Navegação Intuitiva**: Menus e rotas para facilitar o uso.
- **Funcionalidades Avançadas**: 
  - Sistema de avaliações e comentários
  - Cupons de desconto
  - Cálculo automático de frete e impostos
  - Múltiplas formas de pagamento (cartão, PIX, boleto)

## Tecnologias Utilizadas

- **Back-end**: Python, Django, Django REST Framework
- **Front-end**: React, Vite, React Router DOM
- **Banco de Dados**: PostgreSQL (produção), SQLite (desenvolvimento)
- **Estilização**: Tailwind CSS (via shadcn/ui)
- **Gerenciador de Pacotes**: pnpm (Node.js)

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
