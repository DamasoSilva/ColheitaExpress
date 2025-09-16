from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Order(models.Model):
    """
    Modelo para pedidos do e-commerce.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('processing', 'Processando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
        ('returned', 'Devolvido'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('cash_on_delivery', 'Dinheiro na Entrega'),
    ]
    
    # Identificação única
    order_number = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        verbose_name='Número do Pedido'
    )
    
    # Relacionamentos
    customer = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name='Cliente'
    )
    
    # Status do pedido
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Status'
    )
    
    # Informações de pagamento
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending',
        verbose_name='Status do Pagamento'
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Método de Pagamento'
    )
    
    # Valores
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Subtotal'
    )
    shipping_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Custo de Envio'
    )
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Desconto'
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Total'
    )
    
    # Endereço de entrega
    shipping_address = models.TextField(verbose_name='Endereço de Entrega')
    shipping_city = models.CharField(max_length=100, verbose_name='Cidade')
    shipping_state = models.CharField(max_length=100, verbose_name='Estado')
    shipping_postal_code = models.CharField(max_length=10, verbose_name='CEP')
    shipping_country = models.CharField(max_length=100, default='Brasil', verbose_name='País')
    
    # Observações
    notes = models.TextField(blank=True, verbose_name='Observações')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Confirmado em')
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name='Enviado em')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Entregue em')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido {self.order_number} - {self.customer.full_name}"
    
    @property
    def total_items(self):
        """Retorna o número total de itens no pedido"""
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    def calculate_total(self):
        """Calcula o total do pedido"""
        self.total = self.subtotal + self.shipping_cost - self.discount
        return self.total
    
    def get_full_shipping_address(self):
        """Retorna o endereço de entrega completo formatado"""
        return f"{self.shipping_address}, {self.shipping_city}, {self.shipping_state}, {self.shipping_postal_code}, {self.shipping_country}"


class OrderItem(models.Model):
    """
    Modelo para itens de um pedido.
    """
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='Pedido'
    )
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.CASCADE,
        verbose_name='Produto'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço Unitário'
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço Total'
    )
    
    # Informações do produto no momento da compra (para histórico)
    product_name = models.CharField(max_length=200, verbose_name='Nome do Produto')
    product_description = models.TextField(verbose_name='Descrição do Produto')
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens dos Pedidos'
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name} - Pedido {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        """Calcula o preço total automaticamente"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """
    Modelo para histórico de mudanças de status dos pedidos.
    """
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='status_history',
        verbose_name='Pedido'
    )
    status = models.CharField(
        max_length=20, 
        choices=Order.STATUS_CHOICES,
        verbose_name='Status'
    )
    notes = models.TextField(blank=True, verbose_name='Observações')
    changed_by = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Alterado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido {self.order.order_number} - {self.get_status_display()}"


class Cart(models.Model):
    """
    Modelo para carrinho de compras.
    """
    customer = models.OneToOneField(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='cart',
        verbose_name='Cliente'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'
    
    def __str__(self):
        return f"Carrinho de {self.customer.full_name}"
    
    @property
    def total_items(self):
        """Retorna o número total de itens no carrinho"""
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    @property
    def total_price(self):
        """Calcula o preço total do carrinho"""
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(models.Model):
    """
    Modelo para itens do carrinho de compras.
    """
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='Carrinho'
    )
    product = models.ForeignKey(
        'products.Product', 
        on_delete=models.CASCADE,
        verbose_name='Produto'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Adicionado em')
    
    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} - Carrinho de {self.cart.customer.full_name}"
    
    @property
    def unit_price(self):
        """Retorna o preço unitário atual do produto"""
        return self.product.current_price
    
    @property
    def total_price(self):
        """Calcula o preço total do item"""
        return self.quantity * self.unit_price
