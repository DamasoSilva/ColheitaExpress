from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer
from users.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer para itens do pedido
    """
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'unit_price', 'subtotal'
        ]
        read_only_fields = ['id', 'unit_price']
    
    def get_subtotal(self, obj):
        return obj.quantity * obj.unit_price


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de pedidos
    """
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer_name', 'status', 'total_amount',
            'items_count', 'created_at', 'estimated_delivery'
        ]
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo para detalhes do pedido
    """
    customer = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'customer', 'status', 'items',
            'subtotal', 'shipping_cost', 'tax_amount', 'discount_amount',
            'total_amount', 'shipping_address', 'billing_address',
            'payment_method', 'payment_status', 'notes',
            'created_at', 'updated_at', 'estimated_delivery'
        ]
        read_only_fields = [
            'id', 'order_number', 'created_at', 'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de pedidos
    """
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'shipping_address', 'billing_address', 'payment_method',
            'notes', 'items'
        ]
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("O pedido deve ter pelo menos um item.")
        
        # Verificar se todos os produtos existem e estão ativos
        from products.models import Product
        for item_data in value:
            try:
                product = Product.objects.get(id=item_data['product_id'])
                if not product.is_active:
                    raise serializers.ValidationError(
                        f"O produto {product.name} não está disponível."
                    )
                
                # Verificar estoque
                if product.stock_quantity < item_data['quantity']:
                    raise serializers.ValidationError(
                        f"Estoque insuficiente para {product.name}. "
                        f"Disponível: {product.stock_quantity}, Solicitado: {item_data['quantity']}"
                    )
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Produto com ID {item_data['product_id']} não encontrado."
                )
        
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Criar o pedido
        order = Order.objects.create(
            customer=self.context['request'].user,
            **validated_data
        )
        
        # Criar os itens do pedido
        from products.models import Product
        subtotal = 0
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            
            # Usar preço atual do produto (ou preço promocional se houver)
            unit_price = product.get_discounted_price()
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=unit_price
            )
            
            subtotal += order_item.quantity * order_item.unit_price
        
        # Calcular valores do pedido
        order.subtotal = subtotal
        order.shipping_cost = order.calculate_shipping_cost()
        order.tax_amount = order.calculate_tax()
        order.total_amount = order.subtotal + order.shipping_cost + order.tax_amount - order.discount_amount
        order.save()
        
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de pedidos (apenas admin)
    """
    class Meta:
        model = Order
        fields = [
            'status', 'payment_status', 'shipping_address', 'billing_address',
            'shipping_cost', 'tax_amount', 'discount_amount', 'notes',
            'estimated_delivery'
        ]
    
    def validate_status(self, value):
        instance = getattr(self, 'instance', None)
        if instance:
            current_status = instance.status
            
            # Regras de transição de status
            valid_transitions = {
                'pending': ['confirmed', 'cancelled'],
                'confirmed': ['processing', 'cancelled'],
                'processing': ['shipped', 'cancelled'],
                'shipped': ['delivered', 'returned'],
                'delivered': ['returned'],
                'cancelled': [],  # Status final
                'returned': []   # Status final
            }
            
            if value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Transição de status inválida: {current_status} -> {value}"
                )
        
        return value


class OrderStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer para atualização de status do pedido
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
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_status(self, value):
        order = self.context.get('order')
        if order:
            current_status = order.status
            
            # Regras de transição de status
            valid_transitions = {
                'pending': ['confirmed', 'cancelled'],
                'confirmed': ['processing', 'cancelled'],
                'processing': ['shipped', 'cancelled'],
                'shipped': ['delivered', 'returned'],
                'delivered': ['returned'],
                'cancelled': [],  # Status final
                'returned': []   # Status final
            }
            
            if value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Transição de status inválida: {current_status} -> {value}"
                )
        
        return value


class OrderSearchSerializer(serializers.Serializer):
    """
    Serializer para busca de pedidos
    """
    order_number = serializers.CharField(required=False, allow_blank=True)
    customer_name = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    payment_status = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    min_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    ordering = serializers.ChoiceField(
        choices=[
            'created_at', '-created_at', 'total_amount', '-total_amount',
            'status', '-status'
        ],
        required=False,
        default='-created_at'
    )


class OrderReportSerializer(serializers.Serializer):
    """
    Serializer para relatórios de pedidos
    """
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField(required=False)
    customer = serializers.IntegerField(required=False)
    
    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "A data de início deve ser anterior à data de fim."
            )
        
        return attrs


class CartItemSerializer(serializers.Serializer):
    """
    Serializer para itens do carrinho (temporário)
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, value):
        from products.models import Product
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produto não encontrado ou inativo.")
        return value


class CartSerializer(serializers.Serializer):
    """
    Serializer para carrinho de compras
    """
    items = CartItemSerializer(many=True)
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("O carrinho deve ter pelo menos um item.")
        
        # Verificar duplicatas
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Produtos duplicados no carrinho.")
        
        return value
