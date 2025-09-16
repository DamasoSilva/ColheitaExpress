# Guia de Deploy - ColheitaExpress

Este guia fornece instruções detalhadas para fazer o deploy da plataforma ColheitaExpress em diferentes ambientes.

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Deploy com Docker (Recomendado)](#deploy-com-docker-recomendado)
- [Deploy Manual](#deploy-manual)
- [Deploy em Produção](#deploy-em-produção)
- [Configuração de SSL](#configuração-de-ssl)
- [Monitoramento](#monitoramento)
- [Backup e Restore](#backup-e-restore)
- [Troubleshooting](#troubleshooting)

## 🔧 Pré-requisitos

### Requisitos Mínimos do Servidor

- **CPU**: 2 cores
- **RAM**: 4GB
- **Armazenamento**: 20GB SSD
- **Sistema Operacional**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+

### Software Necessário

- Docker 20.10+
- Docker Compose 2.0+
- Git
- Nginx (para proxy reverso)
- Certbot (para SSL)

### Instalação do Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## 🐳 Deploy com Docker (Recomendado)

### 1. Preparação do Ambiente

```bash
# Clone o repositório
git clone https://github.com/DamasoSilva/ColheitaExpress.git
cd ColheitaExpress

# Configure as variáveis de ambiente
cp .env.example .env
nano .env  # Edite com suas configurações
```

### 2. Configuração das Variáveis de Ambiente

Edite o arquivo `.env` com suas configurações:

```env
# Configurações essenciais
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com

# Banco de dados
DATABASE_URL=postgresql://postgres:senha-segura@db:5432/colheitaexpress

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app

# Pagamentos
STRIPE_SECRET_KEY=sk_live_sua-chave-stripe
```

### 3. Deploy Automatizado

```bash
# Execute o script de deploy
./scripts/deploy.sh deploy
```

O script irá:
- Verificar dependências
- Construir as imagens Docker
- Iniciar os serviços
- Executar migrações
- Coletar arquivos estáticos
- Criar usuário administrador
- Verificar a saúde dos serviços

### 4. Verificação

```bash
# Verificar status dos serviços
./scripts/deploy.sh status

# Verificar saúde dos serviços
./scripts/deploy.sh health

# Ver logs
./scripts/deploy.sh logs
```

## 🔧 Deploy Manual

### 1. Configuração do Backend

```bash
cd backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Instalar Gunicorn
pip install gunicorn

# Criar arquivo de serviço systemd
sudo nano /etc/systemd/system/colheitaexpress-backend.service
```

Conteúdo do arquivo de serviço:

```ini
[Unit]
Description=ColheitaExpress Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/ColheitaExpress/backend
Environment="PATH=/path/to/ColheitaExpress/backend/venv/bin"
EnvironmentFile=/path/to/ColheitaExpress/.env
ExecStart=/path/to/ColheitaExpress/backend/venv/bin/gunicorn --workers 3 --bind unix:/run/colheitaexpress.sock ecommerce_saas.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. Configuração do Frontend

```bash
cd frontend/ecommerce-frontend

# Instalar dependências
npm install

# Build para produção
npm run build

# Copiar arquivos para servidor web
sudo cp -r dist/* /var/www/colheitaexpress/
```

### 3. Configuração do Nginx

```bash
sudo nano /etc/nginx/sites-available/colheitaexpress
```

Conteúdo da configuração:

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location /static/ {
        alias /path/to/ColheitaExpress/backend/static/;
    }

    location /media/ {
        alias /path/to/ColheitaExpress/backend/media/;
    }

    location /api/ {
        proxy_pass http://unix:/run/colheitaexpress.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /var/www/colheitaexpress;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/colheitaexpress /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Deploy em Produção

### 1. Configurações de Segurança

```bash
# Configurar firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Configurar fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### 2. Configuração de SSL

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Configurar renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Configuração de Backup

```bash
# Criar script de backup
sudo nano /usr/local/bin/backup-colheitaexpress.sh
```

Conteúdo do script:

```bash
#!/bin/bash
BACKUP_DIR="/backups/colheitaexpress"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do banco de dados
docker-compose exec -T db pg_dump -U postgres colheitaexpress > $BACKUP_DIR/db_$DATE.sql

# Backup dos arquivos de mídia
tar -czf $BACKUP_DIR/media_$DATE.tar.gz backend/media/

# Remover backups antigos (manter 30 dias)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/backup-colheitaexpress.sh

# Configurar cron para backup diário
sudo crontab -e
# Adicionar: 0 2 * * * /usr/local/bin/backup-colheitaexpress.sh
```

## 📊 Monitoramento

### 1. Logs

```bash
# Ver logs do Docker
docker-compose logs -f

# Ver logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend

# Ver logs do sistema
sudo journalctl -u colheitaexpress-backend -f
```

### 2. Métricas

```bash
# Verificar uso de recursos
docker stats

# Verificar espaço em disco
df -h

# Verificar memória
free -h

# Verificar processos
htop
```

### 3. Health Checks

```bash
# Verificar saúde dos serviços
curl http://localhost:8000/health/
curl http://localhost:3000/health

# Verificar banco de dados
docker-compose exec db pg_isready -U postgres

# Verificar Redis
docker-compose exec redis redis-cli ping
```

## 💾 Backup e Restore

### Backup

```bash
# Backup automático via script
./scripts/deploy.sh backup

# Backup manual
docker-compose exec -T db pg_dump -U postgres colheitaexpress > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
# Restore via script
./scripts/deploy.sh restore backup_20240916.sql

# Restore manual
docker-compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS colheitaexpress;"
docker-compose exec -T db psql -U postgres -c "CREATE DATABASE colheitaexpress;"
docker-compose exec -T db psql -U postgres colheitaexpress < backup_20240916.sql
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Serviço não inicia

```bash
# Verificar logs
docker-compose logs backend

# Verificar configurações
docker-compose config

# Reconstruir imagens
docker-compose build --no-cache
```

#### 2. Erro de conexão com banco

```bash
# Verificar se o banco está rodando
docker-compose ps db

# Verificar logs do banco
docker-compose logs db

# Testar conexão
docker-compose exec backend python manage.py dbshell
```

#### 3. Problemas de permissão

```bash
# Corrigir permissões
sudo chown -R www-data:www-data /path/to/ColheitaExpress/
sudo chmod -R 755 /path/to/ColheitaExpress/
```

#### 4. Erro 502 Bad Gateway

```bash
# Verificar se o backend está rodando
curl http://localhost:8000/health/

# Verificar configuração do Nginx
sudo nginx -t

# Verificar logs do Nginx
sudo tail -f /var/log/nginx/error.log
```

### Comandos Úteis

```bash
# Reiniciar todos os serviços
./scripts/deploy.sh restart

# Parar todos os serviços
./scripts/deploy.sh stop

# Atualizar aplicação
./scripts/deploy.sh update

# Limpar containers e volumes
docker-compose down -v
docker system prune -a
```

## 📞 Suporte

Para problemas não resolvidos por este guia:

1. Verifique os logs detalhados
2. Consulte a documentação da API
3. Abra uma issue no GitHub
4. Entre em contato com o suporte técnico

---

**Nota**: Sempre teste o deploy em um ambiente de desenvolvimento antes de aplicar em produção.

