from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging
import requests
from decimal import Decimal

User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, message, recipient_list, html_message=None, from_email=None):
    """
    Tarefa assíncrona para envio de emails
    """
    try:
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL
        
        if html_message:
            # Enviar email com HTML
            msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
        else:
            # Enviar email simples
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False
            )
        
        logger.info(f"Email sent successfully to {recipient_list}")
        return f"Email sent to {len(recipient_list)} recipients"
        
    except Exception as exc:
        logger.error(f"Error sending email: {exc}")
        # Retry com backoff exponencial
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def send_welcome_email(user_id):
    """
    Enviar email de boas-vindas para novo usuário
    """
    try:
        user = User.objects.get(id=user_id)
        
        subject = 'Bem-vindo ao ColheitaExpress!'
        
        # Renderizar template HTML
        html_message = render_to_string('emails/welcome.html', {
            'user': user,
            'site_url': settings.FRONTEND_URL
        })
        
        # Mensagem em texto simples
        message = f"""
        Olá {user.full_name},
        
        Bem-vindo ao ColheitaExpress! Sua conta foi criada com sucesso.
        
        Você pode acessar sua conta em: {settings.FRONTEND_URL}
        
        Atenciosamente,
        Equipe ColheitaExpress
        """
        
        send_email_task.delay(
            subject=subject,
            message=message,
            recipient_list=[user.email],
            html_message=html_message
        )
        
        logger.info(f"Welcome email queued for user {user.email}")
        
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
    except Exception as e:
        logger.error(f"Error sending welcome email: {e}")


@shared_task
def send_order_confirmation_email(order_id):
    """
    Enviar email de confirmação de pedido
    """
    try:
        from orders.models import Order
        
        order = Order.objects.select_related('customer').prefetch_related('items__product').get(id=order_id)
        
        subject = f'Confirmação do Pedido #{order.order_number}'
        
        # Renderizar template HTML
        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'customer': order.customer,
            'site_url': settings.FRONTEND_URL
        })
        
        # Mensagem em texto simples
        message = f"""
        Olá {order.customer.full_name},
        
        Seu pedido #{order.order_number} foi confirmado!
        
        Total: R$ {order.total_amount}
        Status: {order.get_status_display()}
        
        Você pode acompanhar seu pedido em: {settings.FRONTEND_URL}/orders/{order.id}
        
        Atenciosamente,
        Equipe ColheitaExpress
        """
        
        send_email_task.delay(
            subject=subject,
            message=message,
            recipient_list=[order.customer.email],
            html_message=html_message
        )
        
        logger.info(f"Order confirmation email queued for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Error sending order confirmation email: {e}")


@shared_task
def send_order_status_update_email(order_id, old_status, new_status):
    """
    Enviar email de atualização de status do pedido
    """
    try:
        from orders.models import Order
        
        order = Order.objects.select_related('customer').get(id=order_id)
        
        subject = f'Atualização do Pedido #{order.order_number}'
        
        # Renderizar template HTML
        html_message = render_to_string('emails/order_status_update.html', {
            'order': order,
            'customer': order.customer,
            'old_status': old_status,
            'new_status': new_status,
            'site_url': settings.FRONTEND_URL
        })
        
        # Mensagem em texto simples
        message = f"""
        Olá {order.customer.full_name},
        
        O status do seu pedido #{order.order_number} foi atualizado.
        
        Status anterior: {old_status}
        Novo status: {new_status}
        
        Você pode acompanhar seu pedido em: {settings.FRONTEND_URL}/orders/{order.id}
        
        Atenciosamente,
        Equipe ColheitaExpress
        """
        
        send_email_task.delay(
            subject=subject,
            message=message,
            recipient_list=[order.customer.email],
            html_message=html_message
        )
        
        logger.info(f"Order status update email queued for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Error sending order status update email: {e}")


@shared_task(bind=True, max_retries=3)
def process_payment_task(self, payment_id):
    """
    Processar pagamento de forma assíncrona
    """
    try:
        from payments.models import Payment
        
        payment = Payment.objects.select_related('order').get(id=payment_id)
        
        # Simular processamento de pagamento
        # Em produção, aqui seria a integração com gateway de pagamento
        
        if payment.payment_method == 'credit_card':
            # Processar cartão de crédito
            success = self._process_credit_card_payment(payment)
        elif payment.payment_method == 'pix':
            # Processar PIX
            success = self._process_pix_payment(payment)
        elif payment.payment_method == 'bank_slip':
            # Gerar boleto
            success = self._generate_bank_slip(payment)
        else:
            success = False
        
        if success:
            payment.status = 'completed'
            payment.processed_at = timezone.now()
            payment.save()
            
            # Atualizar status do pedido
            order = payment.order
            order.status = 'confirmed'
            order.save()
            
            # Enviar email de confirmação
            send_order_confirmation_email.delay(order.id)
            
            logger.info(f"Payment {payment.id} processed successfully")
            return f"Payment {payment.id} completed"
        else:
            payment.status = 'failed'
            payment.save()
            
            logger.error(f"Payment {payment.id} failed")
            return f"Payment {payment.id} failed"
            
    except Exception as exc:
        logger.error(f"Error processing payment {payment_id}: {exc}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
    
    def _process_credit_card_payment(self, payment):
        """Simular processamento de cartão de crédito"""
        # Em produção, integrar com Stripe, PagSeguro, etc.
        return True
    
    def _process_pix_payment(self, payment):
        """Simular processamento PIX"""
        # Em produção, integrar com banco ou gateway PIX
        return True
    
    def _generate_bank_slip(self, payment):
        """Simular geração de boleto"""
        # Em produção, integrar com banco para gerar boleto
        return True


@shared_task
def update_stock_task(product_id, quantity, movement_type, reason):
    """
    Atualizar estoque de forma assíncrona
    """
    try:
        from products.models import Product, Stock
        
        product = Product.objects.get(id=product_id)
        
        Stock.objects.create(
            product=product,
            quantity=quantity,
            movement_type=movement_type,
            reason=reason
        )
        
        logger.info(f"Stock updated for product {product.name}: {movement_type} {quantity}")
        return f"Stock updated for product {product_id}"
        
    except Exception as e:
        logger.error(f"Error updating stock: {e}")
        raise


@shared_task
def generate_sales_report_task(start_date, end_date, user_id):
    """
    Gerar relatório de vendas de forma assíncrona
    """
    try:
        from orders.models import Order
        from django.db.models import Sum, Count
        
        user = User.objects.get(id=user_id)
        
        # Consultar pedidos no período
        orders = Order.objects.filter(
            created_at__date__range=[start_date, end_date],
            status__in=['confirmed', 'shipped', 'delivered']
        )
        
        # Calcular métricas
        total_orders = orders.count()
        total_revenue = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        
        # Gerar relatório
        report_data = {
            'period': f"{start_date} a {end_date}",
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'average_order_value': float(total_revenue / total_orders) if total_orders > 0 else 0,
        }
        
        # Enviar relatório por email
        subject = f'Relatório de Vendas - {start_date} a {end_date}'
        message = f"""
        Relatório de Vendas
        
        Período: {start_date} a {end_date}
        Total de Pedidos: {total_orders}
        Receita Total: R$ {total_revenue}
        Ticket Médio: R$ {report_data['average_order_value']:.2f}
        
        Atenciosamente,
        Sistema ColheitaExpress
        """
        
        send_email_task.delay(
            subject=subject,
            message=message,
            recipient_list=[user.email]
        )
        
        logger.info(f"Sales report generated for period {start_date} to {end_date}")
        return report_data
        
    except Exception as e:
        logger.error(f"Error generating sales report: {e}")
        raise


@shared_task
def cleanup_expired_sessions_task():
    """
    Limpar sessões expiradas
    """
    try:
        from django.contrib.sessions.models import Session
        
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()
        
        logger.info(f"Cleaned up {count} expired sessions")
        return f"Cleaned up {count} expired sessions"
        
    except Exception as e:
        logger.error(f"Error cleaning up sessions: {e}")
        raise


@shared_task
def backup_database_task():
    """
    Fazer backup do banco de dados
    """
    try:
        import subprocess
        import os
        from datetime import datetime
        
        # Gerar nome do arquivo de backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.sql"
        backup_path = os.path.join(settings.BASE_DIR, 'backups', backup_filename)
        
        # Criar diretório de backup se não existir
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Executar backup (exemplo para PostgreSQL)
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            cmd = [
                'pg_dump',
                '-h', settings.DATABASES['default']['HOST'],
                '-U', settings.DATABASES['default']['USER'],
                '-d', settings.DATABASES['default']['NAME'],
                '-f', backup_path
            ]
            
            subprocess.run(cmd, check=True, env={
                'PGPASSWORD': settings.DATABASES['default']['PASSWORD']
            })
        
        logger.info(f"Database backup created: {backup_filename}")
        return f"Backup created: {backup_filename}"
        
    except Exception as e:
        logger.error(f"Error creating database backup: {e}")
        raise


@shared_task
def send_newsletter_task(newsletter_id):
    """
    Enviar newsletter para lista de usuários
    """
    try:
        # Implementar envio de newsletter
        # Buscar usuários que aceitaram receber emails
        subscribers = User.objects.filter(
            is_active=True,
            # newsletter_subscription=True  # Campo a ser adicionado
        )
        
        # Enviar em lotes para não sobrecarregar o servidor de email
        batch_size = 50
        for i in range(0, subscribers.count(), batch_size):
            batch = subscribers[i:i + batch_size]
            
            for user in batch:
                # Enviar newsletter individual
                send_email_task.delay(
                    subject="Newsletter ColheitaExpress",
                    message="Confira nossas novidades!",
                    recipient_list=[user.email]
                )
        
        logger.info(f"Newsletter {newsletter_id} queued for {subscribers.count()} subscribers")
        return f"Newsletter sent to {subscribers.count()} subscribers"
        
    except Exception as e:
        logger.error(f"Error sending newsletter: {e}")
        raise
