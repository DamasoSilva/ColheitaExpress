import os
from celery import Celery
from django.conf import settings

# Definir o módulo de configurações padrão do Django para o programa 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_saas.settings')

app = Celery('ecommerce_saas')

# Usar uma string aqui significa que o worker não precisa serializar
# o objeto de configuração para processos filhos.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar módulos de tarefas de todas as aplicações Django registradas
app.autodiscover_tasks()

# Configurações adicionais do Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    
    # Configurações de retry
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    
    # Configurações de roteamento
    task_routes={
        'ecommerce_saas.tasks.send_email': {'queue': 'emails'},
        'ecommerce_saas.tasks.process_payment': {'queue': 'payments'},
        'ecommerce_saas.tasks.update_stock': {'queue': 'stock'},
        'ecommerce_saas.tasks.generate_report': {'queue': 'reports'},
    },
    
    # Configurações de beat (tarefas periódicas)
    beat_schedule={
        'cleanup-expired-carts': {
            'task': 'orders.tasks.cleanup_expired_carts',
            'schedule': 3600.0,  # A cada hora
        },
        'update-product-rankings': {
            'task': 'products.tasks.update_product_rankings',
            'schedule': 86400.0,  # Diariamente
        },
        'send-abandoned-cart-emails': {
            'task': 'orders.tasks.send_abandoned_cart_emails',
            'schedule': 7200.0,  # A cada 2 horas
        },
        'cleanup-old-logs': {
            'task': 'audit.tasks.cleanup_old_logs',
            'schedule': 86400.0,  # Diariamente
        },
    },
)


@app.task(bind=True)
def debug_task(self):
    """Tarefa de debug para testar o Celery"""
    print(f'Request: {self.request!r}')
    return 'Debug task completed'


# Configurações de monitoramento
app.conf.worker_send_task_events = True
app.conf.task_send_sent_event = True
