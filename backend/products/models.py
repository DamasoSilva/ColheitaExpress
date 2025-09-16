from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Department(models.Model):
    """
    Modelo para departamentos/categorias de produtos.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='departments/', blank=True, null=True, verbose_name='Imagem')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Modelo para produtos do e-commerce.
    """
    name = models.CharField(max_length=200, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição')
    short_description = models.CharField(max_length=255, blank=True, verbose_name='Descrição Curta')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    
    # Relacionamentos
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='Departamento'
    )
    
    # Preços
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço'
    )
    promotional_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Preço Promocional'
    )
    
    # Imagens
    main_image = models.ImageField(upload_to='products/', verbose_name='Imagem Principal')
    
    # Especificações técnicas
    weight = models.DecimalField(
        max_digits=8, 
        decimal_places=3, 
        blank=True, 
        null=True,
        verbose_name='Peso (kg)'
    )
    dimensions = models.CharField(max_length=100, blank=True, verbose_name='Dimensões')
    
    # Status e controle
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_featured = models.BooleanField(default=False, verbose_name='Produto em Destaque')
    is_on_promotion = models.BooleanField(default=False, verbose_name='Em Promoção')
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name='Meta Título')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta Descrição')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def current_price(self):
        """Retorna o preço atual (promocional se disponível, senão o preço normal)"""
        if self.is_on_promotion and self.promotional_price:
            return self.promotional_price
        return self.price
    
    @property
    def discount_percentage(self):
        """Calcula a porcentagem de desconto se houver promoção"""
        if self.is_on_promotion and self.promotional_price:
            discount = ((self.price - self.promotional_price) / self.price) * 100
            return round(discount, 2)
        return 0
    
    @property
    def stock_quantity(self):
        """Retorna a quantidade total em estoque"""
        return self.stock.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    @property
    def is_in_stock(self):
        """Verifica se o produto está em estoque"""
        return self.stock_quantity > 0


class ProductImage(models.Model):
    """
    Modelo para imagens adicionais dos produtos.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='Produto'
    )
    image = models.ImageField(upload_to='products/gallery/', verbose_name='Imagem')
    alt_text = models.CharField(max_length=255, blank=True, verbose_name='Texto Alternativo')
    order = models.PositiveIntegerField(default=0, verbose_name='Ordem')
    
    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
        ordering = ['order']
    
    def __str__(self):
        return f"Imagem de {self.product.name}"


class Stock(models.Model):
    """
    Modelo para controle de estoque dos produtos.
    """
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Saída'),
        ('adjustment', 'Ajuste'),
    ]
    
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='stock',
        verbose_name='Produto'
    )
    quantity = models.IntegerField(verbose_name='Quantidade')
    movement_type = models.CharField(
        max_length=10, 
        choices=MOVEMENT_TYPES,
        verbose_name='Tipo de Movimento'
    )
    reason = models.CharField(max_length=255, blank=True, verbose_name='Motivo')
    
    # Campos de controle
    created_by = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Criado por'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()}: {self.quantity}"


class ProductReview(models.Model):
    """
    Modelo para avaliações dos produtos pelos clientes.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Produto'
    )
    customer = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Avaliação'
    )
    title = models.CharField(max_length=100, verbose_name='Título')
    comment = models.TextField(verbose_name='Comentário')
    is_approved = models.BooleanField(default=False, verbose_name='Aprovado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-created_at']
        unique_together = ['product', 'customer']
    
    def __str__(self):
        return f"{self.product.name} - {self.rating} estrelas por {self.customer.full_name}"
