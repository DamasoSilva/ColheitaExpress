from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
    OrderStatusUpdateSerializer,
    OrderSearchSerializer,
    OrderReportSerializer,
    CartSerializer
)


class OrderListView(generics.ListAPIView):
    """
    Listar pedidos com filtros
    """
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'customer__full_name']
    ordering_fields = ['created_at', 'total_amount', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('customer')
        
        # Filtrar baseado no tipo de usuário
        if user.user_type == 'admin':
            # Admin vê todos os pedidos
            pass
        elif user.user_type == 'customer':
            # Cliente vê apenas seus pedidos
            queryset = queryset.filter(customer=user)
        else:
            # Outros tipos não têm acesso
            queryset = queryset.none()
        
        return queryset


class OrderDetailView(generics.RetrieveAPIView):
    """
    Visualizar detalhes do pedido
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('customer').prefetch_related('items__product')
        
        # Filtrar baseado no tipo de usuário
        if user.user_type == 'admin':
            return queryset
        elif user.user_type == 'customer':
            return queryset.filter(customer=user)
        else:
            return queryset.none()


class OrderCreateView(generics.CreateAPIView):
    """
    Criar novo pedido (apenas clientes)
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.user_type != 'customer':
            raise permissions.PermissionDenied("Apenas clientes podem criar pedidos.")
        
        order = serializer.save()
        
        # Reduzir estoque dos produtos
        from products.models import Stock
        for item in order.items.all():
            Stock.objects.create(
                product=item.product,
                quantity=item.quantity,
                movement_type='out',
                reason=f'Venda - Pedido {order.order_number}',
                created_by=self.request.user
            )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    """
    Cancelar pedido (cliente ou admin)
    """
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    
    # Verificar permissões
    if user.user_type == 'customer' and order.customer != user:
        raise permissions.PermissionDenied("Você só pode cancelar seus próprios pedidos.")
    elif user.user_type not in ['admin', 'customer']:
        raise permissions.PermissionDenied("Apenas clientes e administradores podem cancelar pedidos.")
    
    # Verificar se o pedido pode ser cancelado
    if order.status in ['delivered', 'cancelled', 'returned']:
        return Response({
            'error': f'Pedido não pode ser cancelado. Status atual: {order.get_status_display()}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Cancelar pedido
    order.status = 'cancelled'
    order.save()
    
    # Devolver estoque
    from products.models import Stock
    for item in order.items.all():
        Stock.objects.create(
            product=item.product,
            quantity=item.quantity,
            movement_type='in',
            reason=f'Cancelamento - Pedido {order.order_number}',
            created_by=user
        )
    
    return Response({
        'message': 'Pedido cancelado com sucesso',
        'order_number': order.order_number
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_cart_total(request):
    """
    Calcular total do carrinho antes de finalizar pedido
    """
    if request.user.user_type != 'customer':
        raise permissions.PermissionDenied("Apenas clientes podem usar o carrinho.")
    
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        items = serializer.validated_data['items']
        
        from products.models import Product
        cart_total = 0
        cart_items = []
        
        for item_data in items:
            try:
                product = Product.objects.get(id=item_data['product_id'], is_active=True)
                quantity = item_data['quantity']
                
                # Verificar estoque
                if product.stock_quantity < quantity:
                    return Response({
                        'error': f'Estoque insuficiente para {product.name}. '
                                f'Disponível: {product.stock_quantity}, Solicitado: {quantity}'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                unit_price = product.get_discounted_price()
                subtotal = unit_price * quantity
                cart_total += subtotal
                
                cart_items.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'quantity': quantity,
                    'unit_price': float(unit_price),
                    'subtotal': float(subtotal)
                })
                
            except Product.DoesNotExist:
                return Response({
                    'error': f'Produto com ID {item_data["product_id"]} não encontrado.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcular custos adicionais (simulado)
        shipping_cost = 15.00 if cart_total < 100 else 0  # Frete grátis acima de R$ 100
        tax_amount = cart_total * 0.05  # 5% de impostos
        total_amount = cart_total + shipping_cost + tax_amount
        
        return Response({
            'items': cart_items,
            'subtotal': float(cart_total),
            'shipping_cost': float(shipping_cost),
            'tax_amount': float(tax_amount),
            'total_amount': float(total_amount)
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
