from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Delivery(models.Model):
    """
    Modelo para entregas dos pedidos.
    """
    STATUS_CHOICES = [
        ('assigned', 'Atribuída'),
        ('picked_up', 'Coletada'),
        ('in_transit', 'Em Trânsito'),
        ('delivered', 'Entregue'),
        ('failed', 'Falha na Entrega'),
        ('returned', 'Devolvida'),
    ]
    
    # Identificação única
    tracking_code = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        verbose_name='Código de Rastreamento'
    )
    
    # Relacionamentos
    order = models.OneToOneField(
        'orders.Order', 
        on_delete=models.CASCADE, 
        related_name='delivery',
        verbose_name='Pedido'
    )
    driver = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='deliveries',
        limit_choices_to={'user_type': 'driver'},
        verbose_name='Motorista'
    )
    
    # Status da entrega
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='assigned',
        verbose_name='Status'
    )
    
    # Informações de entrega
    estimated_delivery_date = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Data Estimada de Entrega'
    )
    actual_delivery_date = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Data Real de Entrega'
    )
    
    # Endereço de entrega (copiado do pedido para histórico)
    delivery_address = models.TextField(verbose_name='Endereço de Entrega')
    delivery_city = models.CharField(max_length=100, verbose_name='Cidade')
    delivery_state = models.CharField(max_length=100, verbose_name='Estado')
    delivery_postal_code = models.CharField(max_length=10, verbose_name='CEP')
    delivery_country = models.CharField(max_length=100, default='Brasil', verbose_name='País')
    
    # Informações do cliente (para o motorista)
    customer_name = models.CharField(max_length=255, verbose_name='Nome do Cliente')
    customer_phone = models.CharField(max_length=17, verbose_name='Telefone do Cliente')
    
    # Observações e instruções
    delivery_instructions = models.TextField(
        blank=True, 
        verbose_name='Instruções de Entrega'
    )
    delivery_notes = models.TextField(
        blank=True, 
        verbose_name='Observações da Entrega'
    )
    
    # Assinatura e confirmação
    recipient_name = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name='Nome do Recebedor'
    )
    signature_image = models.ImageField(
        upload_to='delivery_signatures/', 
        blank=True, 
        null=True,
        verbose_name='Imagem da Assinatura'
    )
    delivery_photo = models.ImageField(
        upload_to='delivery_photos/', 
        blank=True, 
        null=True,
        verbose_name='Foto da Entrega'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    assigned_at = models.DateTimeField(null=True, blank=True, verbose_name='Atribuído em')
    picked_up_at = models.DateTimeField(null=True, blank=True, verbose_name='Coletado em')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Entregue em')
    
    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Entrega {self.tracking_code} - Pedido {self.order.order_number}"
    
    def get_full_delivery_address(self):
        """Retorna o endereço de entrega completo formatado"""
        return f"{self.delivery_address}, {self.delivery_city}, {self.delivery_state}, {self.delivery_postal_code}, {self.delivery_country}"
    
    @property
    def is_completed(self):
        """Verifica se a entrega foi concluída"""
        return self.status in ['delivered', 'returned']
    
    @property
    def delivery_items_summary(self):
        """Retorna um resumo dos itens para entrega"""
        items = []
        for item in self.order.items.all():
            items.append(f"{item.quantity}x {item.product_name}")
        return items


class DeliveryStatusHistory(models.Model):
    """
    Modelo para histórico de mudanças de status das entregas.
    """
    delivery = models.ForeignKey(
        Delivery, 
        on_delete=models.CASCADE, 
        related_name='status_history',
        verbose_name='Entrega'
    )
    status = models.CharField(
        max_length=20, 
        choices=Delivery.STATUS_CHOICES,
        verbose_name='Status'
    )
    notes = models.TextField(blank=True, verbose_name='Observações')
    location = models.CharField(max_length=255, blank=True, verbose_name='Localização')
    
    # Coordenadas GPS (opcional)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Latitude'
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        verbose_name='Longitude'
    )
    
    changed_by = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Alterado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Histórico de Status da Entrega'
        verbose_name_plural = 'Históricos de Status das Entregas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Entrega {self.delivery.tracking_code} - {self.get_status_display()}"


class DeliveryRoute(models.Model):
    """
    Modelo para rotas de entrega dos motoristas.
    """
    driver = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='delivery_routes',
        limit_choices_to={'user_type': 'driver'},
        verbose_name='Motorista'
    )
    date = models.DateField(verbose_name='Data')
    start_time = models.TimeField(null=True, blank=True, verbose_name='Hora de Início')
    end_time = models.TimeField(null=True, blank=True, verbose_name='Hora de Término')
    
    # Informações da rota
    total_deliveries = models.PositiveIntegerField(default=0, verbose_name='Total de Entregas')
    completed_deliveries = models.PositiveIntegerField(default=0, verbose_name='Entregas Concluídas')
    failed_deliveries = models.PositiveIntegerField(default=0, verbose_name='Entregas Falhadas')
    
    # Distância e combustível
    total_distance = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='Distância Total (km)'
    )
    fuel_cost = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='Custo de Combustível'
    )
    
    # Status da rota
    is_completed = models.BooleanField(default=False, verbose_name='Rota Concluída')
    notes = models.TextField(blank=True, verbose_name='Observações')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Rota de Entrega'
        verbose_name_plural = 'Rotas de Entrega'
        ordering = ['-date', '-created_at']
        unique_together = ['driver', 'date']
    
    def __str__(self):
        return f"Rota de {self.driver.full_name} - {self.date}"
    
    @property
    def completion_rate(self):
        """Calcula a taxa de conclusão das entregas"""
        if self.total_deliveries > 0:
            return (self.completed_deliveries / self.total_deliveries) * 100
        return 0


class DeliveryFeedback(models.Model):
    """
    Modelo para feedback dos clientes sobre as entregas.
    """
    delivery = models.OneToOneField(
        Delivery, 
        on_delete=models.CASCADE, 
        related_name='feedback',
        verbose_name='Entrega'
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Avaliação'
    )
    comment = models.TextField(blank=True, verbose_name='Comentário')
    delivery_time_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Avaliação do Tempo de Entrega'
    )
    driver_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Avaliação do Motorista'
    )
    package_condition_rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Avaliação da Condição do Pacote'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Feedback da Entrega'
        verbose_name_plural = 'Feedbacks das Entregas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback da entrega {self.delivery.tracking_code} - {self.rating} estrelas"
