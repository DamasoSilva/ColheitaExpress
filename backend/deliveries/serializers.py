from rest_framework import serializers
from .models import Delivery, DeliveryStatusHistory
from users.serializers import UserSerializer
# from orders.serializers import OrderSerializer  # Evitar import circular


class DeliveryStatusHistorySerializer(serializers.ModelSerializer):
    """
    Serializer para histórico de status de entregas
    """
    class Meta:
        model = DeliveryStatusHistory
        fields = [
            'id', 'delivery', 'status', 'notes', 'changed_at', 'changed_by'
        ]
        read_only_fields = ['id', 'changed_at']


class DeliveryListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem de entregas
    """
    customer_name = serializers.CharField(source='order.customer.full_name', read_only=True)
    customer_phone = serializers.CharField(source='order.customer.phone', read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    driver_name = serializers.CharField(source='driver.full_name', read_only=True)
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone',
            'driver_name', 'status', 'delivery_address', 'estimated_delivery',
            'actual_delivery', 'total_items', 'created_at'
        ]
    
    def get_total_items(self, obj):
        return obj.order.items.count()


class DeliveryDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo para detalhes da entrega
    """
    # order = OrderSerializer(read_only=True)  # Removido para evitar import circular
    driver = UserSerializer(read_only=True)
    status_history = DeliveryStatusHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'driver', 'status', 'delivery_address',
            'delivery_instructions', 'estimated_delivery_date', 'delivery_fee',
            'tracking_code', 'created_at', 'updated_at', 'status_history'
        ]
        read_only_fields = ['id', 'tracking_code', 'created_at', 'updated_at']


class DeliveryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de entregas
    """
    class Meta:
        model = Delivery
        fields = [
            'order', 'driver', 'delivery_address', 'delivery_instructions',
            'estimated_delivery', 'delivery_fee'
        ]
    
    def validate_order(self, value):
        # Verificar se o pedido já tem uma entrega
        if Delivery.objects.filter(order=value).exists():
            raise serializers.ValidationError("Este pedido já possui uma entrega.")
        return value
    
    def validate_driver(self, value):
        # Verificar se o usuário é realmente um motorista
        if value.user_type != 'driver':
            raise serializers.ValidationError("O usuário selecionado não é um motorista.")
        return value


class DeliveryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de entregas
    """
    class Meta:
        model = Delivery
        fields = [
            'driver', 'status', 'delivery_address', 'delivery_instructions',
            'estimated_delivery', 'actual_delivery', 'delivery_fee'
        ]
    
    def validate_status(self, value):
        instance = getattr(self, 'instance', None)
        if instance:
            # Validar transições de status
            current_status = instance.status
            
            # Regras de transição de status
            valid_transitions = {
                'pending': ['assigned', 'cancelled'],
                'assigned': ['in_transit', 'cancelled'],
                'in_transit': ['delivered', 'failed'],
                'delivered': [],  # Status final
                'failed': ['assigned'],  # Pode ser reatribuído
                'cancelled': []  # Status final
            }
            
            if value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Transição de status inválida: {current_status} -> {value}"
                )
        
        return value


class DeliveryDriverSerializer(serializers.ModelSerializer):
    """
    Serializer específico para motoristas (visão limitada)
    """
    customer_name = serializers.CharField(source='order.customer.full_name', read_only=True)
    customer_phone = serializers.CharField(source='order.customer.phone', read_only=True)
    order_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Delivery
        fields = [
            'id', 'tracking_code', 'customer_name', 'customer_phone',
            'delivery_address', 'delivery_instructions', 'estimated_delivery',
            'status', 'order_items'
        ]
        read_only_fields = ['id', 'tracking_code', 'customer_name', 'customer_phone']
    
    def get_order_items(self, obj):
        # Retornar apenas informações básicas dos itens
        items = []
        for item in obj.order.items.all():
            items.append({
                'product_name': item.product.name,
                'quantity': item.quantity,
                'unit_price': item.unit_price
            })
        return items


class DeliveryStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer para atualização de status da entrega
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('assigned', 'Atribuída'),
        ('in_transit', 'Em Trânsito'),
        ('delivered', 'Entregue'),
        ('failed', 'Falha na Entrega'),
        ('cancelled', 'Cancelada'),
    ]
    
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    notes = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_status(self, value):
        delivery = self.context.get('delivery')
        if delivery:
            current_status = delivery.status
            
            # Regras de transição de status
            valid_transitions = {
                'pending': ['assigned', 'cancelled'],
                'assigned': ['in_transit', 'cancelled'],
                'in_transit': ['delivered', 'failed'],
                'delivered': [],  # Status final
                'failed': ['assigned'],  # Pode ser reatribuído
                'cancelled': []  # Status final
            }
            
            if value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Transição de status inválida: {current_status} -> {value}"
                )
        
        return value


class DeliveryStatusHistoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de histórico de status
    """
    class Meta:
        model = DeliveryStatusHistory
        fields = ['delivery', 'status', 'notes']
    
    def create(self, validated_data):
        # Adicionar o usuário que criou o histórico
        validated_data['changed_by'] = self.context['request'].user
        return super().create(validated_data)


class DeliveryReportSerializer(serializers.Serializer):
    """
    Serializer para relatórios de entrega
    """
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    driver = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    
    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "A data de início deve ser anterior à data de fim."
            )
        
        return attrs


class DeliverySearchSerializer(serializers.Serializer):
    """
    Serializer para busca de entregas
    """
    tracking_code = serializers.CharField(required=False, allow_blank=True)
    customer_name = serializers.CharField(required=False, allow_blank=True)
    driver = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    ordering = serializers.ChoiceField(
        choices=[
            'created_at', '-created_at', 'estimated_delivery', '-estimated_delivery',
            'status', '-status'
        ],
        required=False,
        default='-created_at'
    )
