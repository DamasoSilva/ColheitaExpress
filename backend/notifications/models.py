from django.db import models
from django.utils import timezone
import uuid


class NotificationTemplate(models.Model):
    """
    Modelo para templates de notificações.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('order_confirmation', 'Confirmação de Pedido'),
        ('order_status_update', 'Atualização de Status do Pedido'),
        ('delivery_assigned', 'Entrega Atribuída'),
        ('delivery_status_update', 'Atualização de Status da Entrega'),
        ('payment_confirmation', 'Confirmação de Pagamento'),
        ('payment_failed', 'Falha no Pagamento'),
        ('promotion', 'Promoção'),
        ('welcome', 'Boas-vindas'),
        ('password_reset', 'Redefinição de Senha'),
        ('stock_alert', 'Alerta de Estoque'),
        ('review_request', 'Solicitação de Avaliação'),
    ]
    
    CHANNEL_CHOICES = [
        ('email', 'E-mail'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'Notificação no App'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nome')
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPE_CHOICES,
        verbose_name='Tipo de Notificação'
    )
    channel = models.CharField(
        max_length=10,
        choices=CHANNEL_CHOICES,
        verbose_name='Canal'
    )
    
    # Conteúdo do template
    subject = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Assunto'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    content = models.TextField(verbose_name='Conteúdo')
    
    # Configurações
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_default = models.BooleanField(default=False, verbose_name='Padrão')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Template de Notificação'
        verbose_name_plural = 'Templates de Notificações'
        ordering = ['notification_type', 'channel']
        unique_together = ['notification_type', 'channel', 'is_default']
    
    def __str__(self):
        return f"{self.name} ({self.get_channel_display()})"


class Notification(models.Model):
    """
    Modelo para notificações enviadas.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('sent', 'Enviada'),
        ('delivered', 'Entregue'),
        ('failed', 'Falhou'),
        ('read', 'Lida'),
    ]
    
    # Identificação
    notification_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID da Notificação'
    )
    
    # Relacionamentos
    recipient = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinatário'
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Template'
    )
    
    # Conteúdo
    channel = models.CharField(
        max_length=10,
        choices=NotificationTemplate.CHANNEL_CHOICES,
        verbose_name='Canal'
    )
    subject = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Assunto'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Conteúdo')
    
    # Dados adicionais (JSON)
    data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Dados Adicionais'
    )
    
    # Status e controle
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    priority = models.PositiveIntegerField(
        default=1,
        verbose_name='Prioridade'
    )
    
    # Tentativas de envio
    attempts = models.PositiveIntegerField(
        default=0,
        verbose_name='Tentativas'
    )
    max_attempts = models.PositiveIntegerField(
        default=3,
        verbose_name='Máximo de Tentativas'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Enviado em')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Entregue em')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='Lido em')
    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Agendado para'
    )
    
    # Informações de erro
    error_message = models.TextField(
        blank=True,
        verbose_name='Mensagem de Erro'
    )
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'status']),
            models.Index(fields=['channel', 'status']),
            models.Index(fields=['scheduled_for']),
        ]
    
    def __str__(self):
        return f"{self.title} para {self.recipient.full_name}"
    
    @property
    def is_read(self):
        """Verifica se a notificação foi lida"""
        return self.status == 'read'
    
    def mark_as_read(self):
        """Marca a notificação como lida"""
        if self.status in ['sent', 'delivered']:
            self.status = 'read'
            self.read_at = timezone.now()
            self.save(update_fields=['status', 'read_at'])


class NotificationPreference(models.Model):
    """
    Modelo para preferências de notificação dos usuários.
    """
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name='Usuário'
    )
    
    # Preferências por tipo de notificação
    order_updates_email = models.BooleanField(
        default=True,
        verbose_name='Atualizações de Pedido por E-mail'
    )
    order_updates_sms = models.BooleanField(
        default=False,
        verbose_name='Atualizações de Pedido por SMS'
    )
    order_updates_push = models.BooleanField(
        default=True,
        verbose_name='Atualizações de Pedido por Push'
    )
    
    delivery_updates_email = models.BooleanField(
        default=True,
        verbose_name='Atualizações de Entrega por E-mail'
    )
    delivery_updates_sms = models.BooleanField(
        default=True,
        verbose_name='Atualizações de Entrega por SMS'
    )
    delivery_updates_push = models.BooleanField(
        default=True,
        verbose_name='Atualizações de Entrega por Push'
    )
    
    promotions_email = models.BooleanField(
        default=True,
        verbose_name='Promoções por E-mail'
    )
    promotions_sms = models.BooleanField(
        default=False,
        verbose_name='Promoções por SMS'
    )
    promotions_push = models.BooleanField(
        default=False,
        verbose_name='Promoções por Push'
    )
    
    # Configurações gerais
    email_notifications = models.BooleanField(
        default=True,
        verbose_name='Notificações por E-mail'
    )
    sms_notifications = models.BooleanField(
        default=True,
        verbose_name='Notificações por SMS'
    )
    push_notifications = models.BooleanField(
        default=True,
        verbose_name='Push Notifications'
    )
    
    # Horários preferenciais
    quiet_hours_start = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Início do Horário Silencioso'
    )
    quiet_hours_end = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Fim do Horário Silencioso'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Preferência de Notificação'
        verbose_name_plural = 'Preferências de Notificações'
    
    def __str__(self):
        return f"Preferências de {self.user.full_name}"
    
    def can_send_notification(self, channel, notification_type):
        """Verifica se pode enviar notificação baseado nas preferências"""
        # Verificar se o canal está habilitado
        if channel == 'email' and not self.email_notifications:
            return False
        elif channel == 'sms' and not self.sms_notifications:
            return False
        elif channel == 'push' and not self.push_notifications:
            return False
        
        # Verificar preferências específicas por tipo
        if notification_type in ['order_confirmation', 'order_status_update']:
            if channel == 'email':
                return self.order_updates_email
            elif channel == 'sms':
                return self.order_updates_sms
            elif channel == 'push':
                return self.order_updates_push
        
        elif notification_type in ['delivery_assigned', 'delivery_status_update']:
            if channel == 'email':
                return self.delivery_updates_email
            elif channel == 'sms':
                return self.delivery_updates_sms
            elif channel == 'push':
                return self.delivery_updates_push
        
        elif notification_type == 'promotion':
            if channel == 'email':
                return self.promotions_email
            elif channel == 'sms':
                return self.promotions_sms
            elif channel == 'push':
                return self.promotions_push
        
        return True
    
    def is_quiet_hours(self):
        """Verifica se está no horário silencioso"""
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
        
        now = timezone.now().time()
        
        if self.quiet_hours_start <= self.quiet_hours_end:
            return self.quiet_hours_start <= now <= self.quiet_hours_end
        else:  # Horário que cruza meia-noite
            return now >= self.quiet_hours_start or now <= self.quiet_hours_end


class NotificationLog(models.Model):
    """
    Modelo para logs detalhados de notificações.
    """
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='Notificação'
    )
    action = models.CharField(max_length=50, verbose_name='Ação')
    details = models.TextField(blank=True, verbose_name='Detalhes')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    
    class Meta:
        verbose_name = 'Log de Notificação'
        verbose_name_plural = 'Logs de Notificações'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} - {self.notification.title}"

