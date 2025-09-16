from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid
from django.utils import timezone


class Coupon(models.Model):
    """
    Modelo para cupons de desconto.
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Porcentagem'),
        ('fixed', 'Valor Fixo'),
    ]
    
    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='Código do Cupom'
    )
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    
    # Tipo e valor do desconto
    discount_type = models.CharField(
        max_length=10, 
        choices=DISCOUNT_TYPE_CHOICES,
        verbose_name='Tipo de Desconto'
    )
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor do Desconto'
    )
    
    # Valor mínimo do pedido para usar o cupom
    minimum_order_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Mínimo do Pedido'
    )
    
    # Valor máximo de desconto (para cupons de porcentagem)
    maximum_discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Desconto Máximo'
    )
    
    # Limites de uso
    usage_limit = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name='Limite de Uso Total'
    )
    usage_limit_per_customer = models.PositiveIntegerField(
        default=1,
        verbose_name='Limite de Uso por Cliente'
    )
    used_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantidade Usada'
    )
    
    # Datas de validade
    valid_from = models.DateTimeField(verbose_name='Válido a partir de')
    valid_until = models.DateTimeField(verbose_name='Válido até')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    
    # Restrições
    first_order_only = models.BooleanField(
        default=False,
        verbose_name='Apenas Primeiro Pedido'
    )
    
    # Produtos específicos (opcional)
    applicable_products = models.ManyToManyField(
        'products.Product',
        blank=True,
        verbose_name='Produtos Aplicáveis'
    )
    
    # Categorias específicas (opcional)
    applicable_departments = models.ManyToManyField(
        'products.Department',
        blank=True,
        verbose_name='Departamentos Aplicáveis'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Cupom'
        verbose_name_plural = 'Cupons'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_valid(self):
        """Verifica se o cupom está válido"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (self.usage_limit is None or self.used_count < self.usage_limit)
        )
    
    def calculate_discount(self, order_value):
        """Calcula o desconto para um valor de pedido"""
        if not self.is_valid or order_value < self.minimum_order_value:
            return Decimal('0.00')
        
        if self.discount_type == 'percentage':
            discount = (order_value * self.discount_value) / 100
            if self.maximum_discount:
                discount = min(discount, self.maximum_discount)
        else:  # fixed
            discount = self.discount_value
        
        return min(discount, order_value)
    
    def can_be_used_by_customer(self, customer):
        """Verifica se o cupom pode ser usado por um cliente específico"""
        if not self.is_valid:
            return False
        
        # Verificar se é apenas para primeiro pedido
        if self.first_order_only:
            has_previous_orders = customer.orders.filter(
                status__in=['confirmed', 'processing', 'shipped', 'delivered']
            ).exists()
            if has_previous_orders:
                return False
        
        # Verificar limite de uso por cliente
        customer_usage = CouponUsage.objects.filter(
            coupon=self,
            customer=customer
        ).count()
        
        return customer_usage < self.usage_limit_per_customer


class CouponUsage(models.Model):
    """
    Modelo para rastrear o uso de cupons pelos clientes.
    """
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.CASCADE,
        related_name='usages',
        verbose_name='Cupom'
    )
    customer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        verbose_name='Pedido'
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor do Desconto'
    )
    used_at = models.DateTimeField(auto_now_add=True, verbose_name='Usado em')
    
    class Meta:
        verbose_name = 'Uso de Cupom'
        verbose_name_plural = 'Usos de Cupons'
        ordering = ['-used_at']
        unique_together = ['coupon', 'order']
    
    def __str__(self):
        return f"{self.coupon.code} usado por {self.customer.full_name}"


class Promotion(models.Model):
    """
    Modelo para promoções automáticas.
    """
    PROMOTION_TYPE_CHOICES = [
        ('buy_x_get_y', 'Compre X Leve Y'),
        ('bulk_discount', 'Desconto por Quantidade'),
        ('category_discount', 'Desconto por Categoria'),
        ('free_shipping', 'Frete Grátis'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')
    promotion_type = models.CharField(
        max_length=20,
        choices=PROMOTION_TYPE_CHOICES,
        verbose_name='Tipo de Promoção'
    )
    
    # Configurações específicas por tipo
    buy_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Quantidade para Comprar'
    )
    get_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Quantidade Grátis'
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Porcentagem de Desconto'
    )
    minimum_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Quantidade Mínima'
    )
    minimum_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Valor Mínimo'
    )
    
    # Produtos e categorias aplicáveis
    applicable_products = models.ManyToManyField(
        'products.Product',
        blank=True,
        verbose_name='Produtos Aplicáveis'
    )
    applicable_departments = models.ManyToManyField(
        'products.Department',
        blank=True,
        verbose_name='Departamentos Aplicáveis'
    )
    
    # Datas de validade
    valid_from = models.DateTimeField(verbose_name='Válido a partir de')
    valid_until = models.DateTimeField(verbose_name='Válido até')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    priority = models.PositiveIntegerField(
        default=1,
        verbose_name='Prioridade'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Promoção'
        verbose_name_plural = 'Promoções'
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_valid(self):
        """Verifica se a promoção está válida"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until
        )

