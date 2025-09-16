#!/bin/bash

# ColheitaExpress Deploy Script
# Este script automatiza o processo de deploy da aplicação

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "Docker and Docker Compose are installed"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        log_warning ".env file not found. Creating from .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
            log_warning "Please edit .env file with your configuration before continuing"
            read -p "Press Enter to continue after editing .env file..."
        else
            log_error ".env.example file not found. Please create .env file manually."
            exit 1
        fi
    fi
    log_success ".env file found"
}

# Build and start services
deploy_services() {
    log_info "Building and starting services..."
    
    # Stop existing containers
    docker-compose down
    
    # Build images
    log_info "Building Docker images..."
    docker-compose build --no-cache
    
    # Start services
    log_info "Starting services..."
    docker-compose up -d
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    sleep 10
    
    # Run migrations
    log_info "Running database migrations..."
    docker-compose exec -T backend python manage.py migrate
    
    # Collect static files
    log_info "Collecting static files..."
    docker-compose exec -T backend python manage.py collectstatic --noinput
    
    # Create superuser if it doesn't exist
    log_info "Creating superuser (if not exists)..."
    docker-compose exec -T backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@colheitaexpress.com').exists():
    User.objects.create_superuser('admin@colheitaexpress.com', 'admin123')
    print('Superuser created: admin@colheitaexpress.com / admin123')
else:
    print('Superuser already exists')
"
    
    log_success "Services deployed successfully!"
}

# Check service health
check_health() {
    log_info "Checking service health..."
    
    # Check backend health
    if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
        log_success "Backend is healthy"
    else
        log_error "Backend health check failed"
        return 1
    fi
    
    # Check frontend health
    if curl -f http://localhost:3000/ > /dev/null 2>&1; then
        log_success "Frontend is healthy"
    else
        log_error "Frontend health check failed"
        return 1
    fi
    
    # Check database connection
    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        log_success "Database is healthy"
    else
        log_error "Database health check failed"
        return 1
    fi
    
    # Check Redis connection
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis is healthy"
    else
        log_error "Redis health check failed"
        return 1
    fi
    
    log_success "All services are healthy!"
}

# Show service status
show_status() {
    log_info "Service Status:"
    docker-compose ps
    
    echo ""
    log_info "Access URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  Admin Panel: http://localhost:8000/admin"
    echo ""
    log_info "Default Admin Credentials:"
    echo "  Email: admin@colheitaexpress.com"
    echo "  Password: admin123"
    echo ""
    log_warning "Please change the default admin password in production!"
}

# Backup database
backup_database() {
    log_info "Creating database backup..."
    
    BACKUP_DIR="./backups"
    mkdir -p $BACKUP_DIR
    
    BACKUP_FILE="$BACKUP_DIR/colheitaexpress_$(date +%Y%m%d_%H%M%S).sql"
    
    docker-compose exec -T db pg_dump -U postgres colheitaexpress > $BACKUP_FILE
    
    if [ $? -eq 0 ]; then
        log_success "Database backup created: $BACKUP_FILE"
    else
        log_error "Database backup failed"
        return 1
    fi
}

# Restore database from backup
restore_database() {
    if [ -z "$1" ]; then
        log_error "Please provide backup file path"
        echo "Usage: $0 restore <backup_file>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        log_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    log_warning "This will replace the current database. Are you sure? (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        log_info "Database restore cancelled"
        exit 0
    fi
    
    log_info "Restoring database from: $BACKUP_FILE"
    
    # Stop backend services
    docker-compose stop backend celery celery-beat
    
    # Restore database
    docker-compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS colheitaexpress;"
    docker-compose exec -T db psql -U postgres -c "CREATE DATABASE colheitaexpress;"
    docker-compose exec -T db psql -U postgres colheitaexpress < $BACKUP_FILE
    
    # Start backend services
    docker-compose start backend celery celery-beat
    
    log_success "Database restored successfully"
}

# Show logs
show_logs() {
    SERVICE=${1:-""}
    if [ -n "$SERVICE" ]; then
        docker-compose logs -f $SERVICE
    else
        docker-compose logs -f
    fi
}

# Update application
update_app() {
    log_info "Updating application..."
    
    # Pull latest changes
    git pull origin main
    
    # Rebuild and restart services
    deploy_services
    
    log_success "Application updated successfully!"
}

# Main script logic
case "$1" in
    "deploy")
        log_info "Starting ColheitaExpress deployment..."
        check_docker
        check_env_file
        deploy_services
        sleep 5
        check_health
        show_status
        ;;
    "status")
        show_status
        ;;
    "health")
        check_health
        ;;
    "backup")
        backup_database
        ;;
    "restore")
        restore_database "$2"
        ;;
    "logs")
        show_logs "$2"
        ;;
    "update")
        update_app
        ;;
    "stop")
        log_info "Stopping services..."
        docker-compose down
        log_success "Services stopped"
        ;;
    "restart")
        log_info "Restarting services..."
        docker-compose restart
        log_success "Services restarted"
        ;;
    *)
        echo "ColheitaExpress Deploy Script"
        echo ""
        echo "Usage: $0 {deploy|status|health|backup|restore|logs|update|stop|restart}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy the application"
        echo "  status   - Show service status"
        echo "  health   - Check service health"
        echo "  backup   - Create database backup"
        echo "  restore  - Restore database from backup"
        echo "  logs     - Show service logs"
        echo "  update   - Update application from git"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo ""
        echo "Examples:"
        echo "  $0 deploy"
        echo "  $0 logs backend"
        echo "  $0 restore ./backups/backup_20240916.sql"
        exit 1
        ;;
esac

