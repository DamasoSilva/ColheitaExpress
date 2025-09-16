from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import uuid
import json


class AuditLog(models.Model):
    """
    Modelo para logs de auditoria do sistema.
    """
    ACTION_CHOICES = [
        ('create', 'Criação'),
        ('update', 'Atualização'),
        ('delete', 'Exclusão'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Alteração de Senha'),
        ('permission_change', 'Alteração de Permissão'),
        ('status_change', 'Alteração de Status'),
        ('payment', 'Pagamento'),
        ('refund', 'Reembolso'),
        ('delivery', 'Entrega'),
        ('stock_movement', 'Movimentação de Estoque'),
        ('export', 'Exportação'),
        ('import', 'Importação'),
        ('backup', 'Backup'),
        ('restore', 'Restauração'),
        ('api_call', 'Chamada de API'),
        ('error', 'Erro'),
        ('security_event', 'Evento de Segurança'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    ]
    
    # Identificação única
    log_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID do Log'
    )
    
    # Informações do usuário
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário'
    )
    user_email = models.EmailField(
        blank=True,
        verbose_name='E-mail do Usuário'
    )
    user_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP do Usuário'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent'
    )
    
    # Informações da ação
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='Ação'
    )
    description = models.TextField(verbose_name='Descrição')
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='low',
        verbose_name='Severidade'
    )
    
    # Objeto afetado (usando Generic Foreign Key)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Tipo de Conteúdo'
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID do Objeto'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Dados antes e depois da alteração
    old_values = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Valores Antigos'
    )
    new_values = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Valores Novos'
    )
    
    # Metadados adicionais
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Metadados'
    )
    
    # Informações de contexto
    session_id = models.CharField(
        max_length=40,
        blank=True,
        verbose_name='ID da Sessão'
    )
    request_id = models.UUIDField(
        null=True,
        blank=True,
        verbose_name='ID da Requisição'
    )
    
    # Timestamp
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Timestamp'
    )
    
    # Informações técnicas
    module = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Módulo'
    )
    function = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Função'
    )
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['severity', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        user_info = self.user.full_name if self.user else self.user_email or 'Sistema'
        return f"{self.get_action_display()} por {user_info} em {self.timestamp}"
    
    @classmethod
    def log_action(cls, user, action, description, **kwargs):
        """Método helper para criar logs de auditoria"""
        log_data = {
            'user': user,
            'action': action,
            'description': description,
            'severity': kwargs.get('severity', 'low'),
            'old_values': kwargs.get('old_values', {}),
            'new_values': kwargs.get('new_values', {}),
            'metadata': kwargs.get('metadata', {}),
            'user_ip': kwargs.get('user_ip'),
            'user_agent': kwargs.get('user_agent'),
            'session_id': kwargs.get('session_id'),
            'request_id': kwargs.get('request_id'),
            'module': kwargs.get('module'),
            'function': kwargs.get('function'),
        }
        
        # Se há um objeto relacionado
        if 'content_object' in kwargs:
            content_object = kwargs['content_object']
            log_data['content_type'] = ContentType.objects.get_for_model(content_object)
            log_data['object_id'] = content_object.pk
        
        # Armazenar email do usuário para casos onde o usuário é deletado
        if user:
            log_data['user_email'] = user.email
        
        return cls.objects.create(**log_data)


class SecurityEvent(models.Model):
    """
    Modelo para eventos de segurança específicos.
    """
    EVENT_TYPE_CHOICES = [
        ('failed_login', 'Falha de Login'),
        ('multiple_failed_logins', 'Múltiplas Falhas de Login'),
        ('suspicious_activity', 'Atividade Suspeita'),
        ('unauthorized_access', 'Acesso Não Autorizado'),
        ('privilege_escalation', 'Escalação de Privilégios'),
        ('data_breach_attempt', 'Tentativa de Violação de Dados'),
        ('sql_injection', 'Tentativa de SQL Injection'),
        ('xss_attempt', 'Tentativa de XSS'),
        ('csrf_attempt', 'Tentativa de CSRF'),
        ('brute_force', 'Ataque de Força Bruta'),
        ('account_lockout', 'Bloqueio de Conta'),
        ('password_policy_violation', 'Violação de Política de Senha'),
        ('session_hijacking', 'Sequestro de Sessão'),
        ('malware_detected', 'Malware Detectado'),
        ('ddos_attempt', 'Tentativa de DDoS'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Baixo'),
        ('medium', 'Médio'),
        ('high', 'Alto'),
        ('critical', 'Crítico'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Aberto'),
        ('investigating', 'Investigando'),
        ('resolved', 'Resolvido'),
        ('false_positive', 'Falso Positivo'),
        ('ignored', 'Ignorado'),
    ]
    
    # Identificação
    event_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID do Evento'
    )
    
    # Tipo e classificação
    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPE_CHOICES,
        verbose_name='Tipo de Evento'
    )
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVEL_CHOICES,
        verbose_name='Nível de Risco'
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='Status'
    )
    
    # Informações do evento
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descrição')
    
    # Informações do usuário/atacante
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário'
    )
    source_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='IP de Origem'
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name='User Agent'
    )
    
    # Detalhes técnicos
    request_method = models.CharField(
        max_length=10,
        blank=True,
        verbose_name='Método da Requisição'
    )
    request_url = models.URLField(
        blank=True,
        verbose_name='URL da Requisição'
    )
    request_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Dados da Requisição'
    )
    response_status = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Status da Resposta'
    )
    
    # Ações tomadas
    actions_taken = models.TextField(
        blank=True,
        verbose_name='Ações Tomadas'
    )
    blocked = models.BooleanField(
        default=False,
        verbose_name='Bloqueado'
    )
    
    # Timestamps
    detected_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Detectado em'
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Resolvido em'
    )
    
    # Relacionamento com logs de auditoria
    audit_logs = models.ManyToManyField(
        AuditLog,
        blank=True,
        verbose_name='Logs de Auditoria Relacionados'
    )
    
    class Meta:
        verbose_name = 'Evento de Segurança'
        verbose_name_plural = 'Eventos de Segurança'
        ordering = ['-detected_at']
        indexes = [
            models.Index(fields=['event_type', 'detected_at']),
            models.Index(fields=['risk_level', 'status']),
            models.Index(fields=['source_ip', 'detected_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_risk_level_display()}"
    
    def resolve(self, actions_taken=None):
        """Marca o evento como resolvido"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        if actions_taken:
            self.actions_taken = actions_taken
        self.save(update_fields=['status', 'resolved_at', 'actions_taken'])


class SystemMetrics(models.Model):
    """
    Modelo para métricas do sistema.
    """
    METRIC_TYPE_CHOICES = [
        ('performance', 'Performance'),
        ('security', 'Segurança'),
        ('usage', 'Uso'),
        ('error', 'Erro'),
        ('business', 'Negócio'),
    ]
    
    metric_type = models.CharField(
        max_length=15,
        choices=METRIC_TYPE_CHOICES,
        verbose_name='Tipo de Métrica'
    )
    name = models.CharField(max_length=100, verbose_name='Nome')
    value = models.FloatField(verbose_name='Valor')
    unit = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Unidade'
    )
    
    # Metadados
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Metadados'
    )
    
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Timestamp'
    )
    
    class Meta:
        verbose_name = 'Métrica do Sistema'
        verbose_name_plural = 'Métricas do Sistema'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['metric_type', 'name', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.name}: {self.value} {self.unit}"

