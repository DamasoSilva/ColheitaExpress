from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid
from django.utils import timezone


class PaymentMethod(models.Model):
    """
    Modelo para métodos de pagamento disponíveis.
    """
    METHOD_TYPE_CHOICES = [
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('digital_wallet', 'Carteira Digital'),
        ('cash_on_delivery', 'Dinheiro na Entrega'),
        ('bank_slip', 'Boleto Bancário'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nome')
    method_type = models.CharField(
        max_length=20,
        choices=METHOD_TYPE_CHOICES,
        verbose_name='Tipo de Método'
    )
    description = models.TextField(blank=True, verbose_name='Descrição')
    
    # Configurações
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    requires_approval = models.BooleanField(
        default=False,
        verbose_name='Requer Aprovação'
    )
    processing_time_hours = models.PositiveIntegerField(
        default=0,
        verbose_name='Tempo de Processamento (horas)'
    )
    
    # Taxas
    fixed_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Taxa Fixa'
    )
    percentage_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Taxa Percentual'
    )
    
    # Limites
    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor Mínimo'
    )
    maximum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor Máximo'
    )
    
    # Configurações do gateway
    gateway_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nome do Gateway'
    )
    gateway_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Configuração do Gateway'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Método de Pagamento'
        verbose_name_plural = 'Métodos de Pagamento'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def calculate_fee(self, amount):
        """Calcula a taxa para um valor específico"""
        percentage_fee = (amount * self.percentage_fee) / 100
        return self.fixed_fee + percentage_fee
    
    def is_amount_valid(self, amount):
        """Verifica se o valor está dentro dos limites"""
        if self.minimum_amount and amount < self.minimum_amount:
            return False
        if self.maximum_amount and amount > self.maximum_amount:
            return False
        return True


class Payment(models.Model):
    """
    Modelo para pagamentos.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('approved', 'Aprovado'),
        ('declined', 'Recusado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
        ('partially_refunded', 'Parcialmente Reembolsado'),
        ('chargeback', 'Chargeback'),
        ('expired', 'Expirado'),
    ]
    
    # Identificação
    payment_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID do Pagamento'
    )
    
    # Relacionamentos
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Pedido'
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.PROTECT,
        verbose_name='Método de Pagamento'
    )
    
    # Valores
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Taxa'
    )
    net_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Líquido'
    )
    
    # Status e controle
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    # Informações do gateway
    gateway_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID da Transação no Gateway'
    )
    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Resposta do Gateway'
    )
    
    # Informações de cartão (apenas últimos 4 dígitos)
    card_last_four = models.CharField(
        max_length=4,
        blank=True,
        verbose_name='Últimos 4 Dígitos do Cartão'
    )
    card_brand = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Bandeira do Cartão'
    )
    
    # PIX
    pix_qr_code = models.TextField(
        blank=True,
        verbose_name='QR Code PIX'
    )
    pix_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Código PIX'
    )
    
    # Boleto
    bank_slip_url = models.URLField(
        blank=True,
        verbose_name='URL do Boleto'
    )
    bank_slip_barcode = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Código de Barras do Boleto'
    )
    bank_slip_due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Vencimento do Boleto'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Processado em'
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Expira em'
    )
    
    # Observações
    notes = models.TextField(blank=True, verbose_name='Observações')
    failure_reason = models.TextField(
        blank=True,
        verbose_name='Motivo da Falha'
    )
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order', 'status']),
            models.Index(fields=['payment_method', 'status']),
            models.Index(fields=['gateway_transaction_id']),
        ]
    
    def __str__(self):
        return f"Pagamento {self.payment_id} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        """Calcula o valor líquido automaticamente"""
        if not self.net_amount:
            self.net_amount = self.amount - self.fee_amount
        super().save(*args, **kwargs)
    
    @property
    def is_successful(self):
        """Verifica se o pagamento foi bem-sucedido"""
        return self.status == 'approved'
    
    @property
    def can_be_refunded(self):
        """Verifica se o pagamento pode ser reembolsado"""
        return self.status in ['approved'] and self.net_amount > 0


class PaymentRefund(models.Model):
    """
    Modelo para reembolsos de pagamentos.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
    ]
    
    REFUND_TYPE_CHOICES = [
        ('full', 'Total'),
        ('partial', 'Parcial'),
    ]
    
    # Identificação
    refund_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID do Reembolso'
    )
    
    # Relacionamentos
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds',
        verbose_name='Pagamento'
    )
    requested_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Solicitado por'
    )
    
    # Informações do reembolso
    refund_type = models.CharField(
        max_length=10,
        choices=REFUND_TYPE_CHOICES,
        verbose_name='Tipo de Reembolso'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    reason = models.TextField(verbose_name='Motivo')
    
    # Status
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    # Informações do gateway
    gateway_refund_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID do Reembolso no Gateway'
    )
    gateway_response = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Resposta do Gateway'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Processado em'
    )
    
    class Meta:
        verbose_name = 'Reembolso'
        verbose_name_plural = 'Reembolsos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reembolso {self.refund_id} - R$ {self.amount}"


class PaymentInstallment(models.Model):
    """
    Modelo para parcelas de pagamento.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Paga'),
        ('overdue', 'Vencida'),
        ('cancelled', 'Cancelada'),
    ]
    
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='installments',
        verbose_name='Pagamento'
    )
    installment_number = models.PositiveIntegerField(
        verbose_name='Número da Parcela'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    due_date = models.DateField(verbose_name='Data de Vencimento')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    # Informações do gateway
    gateway_installment_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID da Parcela no Gateway'
    )
    
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Paga em'
    )
    
    class Meta:
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['installment_number']
        unique_together = ['payment', 'installment_number']
    
    def __str__(self):
        return f"Parcela {self.installment_number}/{self.payment.installments.count()} - R$ {self.amount}"


class PaymentWebhook(models.Model):
    """
    Modelo para webhooks de pagamento.
    """
    STATUS_CHOICES = [
        ('received', 'Recebido'),
        ('processed', 'Processado'),
        ('failed', 'Falhou'),
        ('ignored', 'Ignorado'),
    ]
    
    # Identificação
    webhook_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID do Webhook'
    )
    
    # Informações do webhook
    gateway_name = models.CharField(
        max_length=50,
        verbose_name='Nome do Gateway'
    )
    event_type = models.CharField(
        max_length=50,
        verbose_name='Tipo de Evento'
    )
    
    # Dados recebidos
    headers = models.JSONField(
        default=dict,
        verbose_name='Cabeçalhos'
    )
    payload = models.JSONField(
        default=dict,
        verbose_name='Payload'
    )
    
    # Processamento
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='received',
        verbose_name='Status'
    )
    processing_result = models.TextField(
        blank=True,
        verbose_name='Resultado do Processamento'
    )
    
    # Relacionamento com pagamento (se identificado)
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='webhooks',
        verbose_name='Pagamento'
    )
    
    # Timestamps
    received_at = models.DateTimeField(auto_now_add=True, verbose_name='Recebido em')
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Processado em'
    )
    
    class Meta:
        verbose_name = 'Webhook de Pagamento'
        verbose_name_plural = 'Webhooks de Pagamento'
        ordering = ['-received_at']
    
    def __str__(self):
        return f"Webhook {self.event_type} - {self.gateway_name}"

