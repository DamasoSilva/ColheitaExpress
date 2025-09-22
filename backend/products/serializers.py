from rest_framework import serializers
from .models import Department, Product, ProductImage, Stock


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer para departamentos
    """
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'products_count']
        read_only_fields = ['id', 'created_at']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer para imagens de produtos
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']
        read_only_fields = ['id']


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer para controle de estoque
    """
    class Meta:
        model = Stock
        fields = [
            'id', 'product', 'quantity', 'movement_type', 'reason', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("A quantidade não pode ser negativa.")
        return value





class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de produtos
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    stock_quantity = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'current_price', 'department_name',
            'primary_image', 'stock_quantity', 'is_in_stock', 'is_active',
            'created_at'
        ]
    
    def get_primary_image(self, obj):
        if obj.main_image:
            return obj.main_image.url
        return None
    
    def get_current_price(self, obj):
        return obj.price
    
    def get_stock_quantity(self, obj):
        return obj.stock_quantity
    
    def get_is_in_stock(self, obj):
        return obj.is_in_stock


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo para detalhes do produto
    """
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stock = StockSerializer(many=True, read_only=True)

    current_price = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'current_price',
            'discount_percentage', 'department', 'department_id',
            'weight', 'dimensions', 'is_active', 'is_featured',
            'meta_title', 'meta_description', 'created_at', 'updated_at',
            'images', 'stock'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
    
    def get_current_price(self, obj):
        return obj.price
    
    def get_discount_percentage(self, obj):
        # Por enquanto sem promoções
        return 0


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e atualização de produtos
    """
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'department',
            'weight', 'dimensions', 'is_active', 'is_featured',
            'meta_title', 'meta_description'
        ]
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser positivo.")
        return value
    



class StockMovementSerializer(serializers.Serializer):
    """
    Serializer para movimentações de estoque
    """
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Saída'),
        ('adjustment', 'Ajuste'),
    ]
    
    product_id = serializers.IntegerField()
    movement_type = serializers.ChoiceField(choices=MOVEMENT_TYPES)
    quantity = serializers.IntegerField(min_value=1)
    reason = serializers.CharField(max_length=255)
    
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produto não encontrado.")
        return value


class ProductSearchSerializer(serializers.Serializer):
    """
    Serializer para busca de produtos
    """
    query = serializers.CharField(required=False, allow_blank=True)
    department = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    in_stock = serializers.BooleanField(required=False)
    is_featured = serializers.BooleanField(required=False)
    ordering = serializers.ChoiceField(
        choices=[
            'name', '-name', 'price', '-price', 'created_at', '-created_at',
            'rating', '-rating'
        ],
        required=False,
        default='-created_at'
    )
