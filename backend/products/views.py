from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Product, ProductImage, Stock
from .serializers import (
    DepartmentSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer,
    StockSerializer,
    StockMovementSerializer,

    ProductSearchSerializer
)


class DepartmentListCreateView(generics.ListCreateAPIView):
    """
    Listar e criar departamentos
    """
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]  # Clientes podem ver departamentos
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]  # Apenas usuários autenticados podem criar
        return [AllowAny()]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Visualizar, atualizar e deletar departamento
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        # Soft delete - marcar como inativo
        instance.is_active = False
        instance.save()


class ProductListView(generics.ListAPIView):
    """
    Listar produtos com filtros e busca
    """
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('department')
        
        # Filtros personalizados
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department_id=department)
        
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            # Filtrar produtos que têm estoque
            from django.db.models import Sum
            queryset = queryset.annotate(
                total_stock=Sum('stock__quantity')
            ).filter(total_stock__gt=0)
        
        is_featured = self.request.query_params.get('is_featured')
        if is_featured and is_featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """
    Visualizar detalhes do produto
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class ProductCreateView(generics.CreateAPIView):
    """
    Criar novo produto (apenas admin)
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Verificar se usuário é admin
        if self.request.user.user_type != 'admin':
            raise permissions.PermissionDenied("Apenas administradores podem criar produtos.")
        
        product = serializer.save()
        
        # Criar registro de estoque inicial
        Stock.objects.create(
            product=product,
            quantity=50,
            movement_type='in',
            reason='Estoque inicial'
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products(request):
    """
    Listar produtos em destaque
    """
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def products_by_department(request, department_id):
    """
    Listar produtos por departamento
    """
    department = get_object_or_404(Department, id=department_id, is_active=True)
    products = Product.objects.filter(department=department, is_active=True)
    serializer = ProductListSerializer(products, many=True)
    return Response({
        'department': DepartmentSerializer(department).data,
        'products': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def inventory_movement(request):
    """
    Registrar movimentação de estoque (apenas admin)
    """
    if request.user.user_type != 'admin':
        raise permissions.PermissionDenied("Apenas administradores podem movimentar estoque.")
    
    serializer = StockMovementSerializer(data=request.data)
    if serializer.is_valid():
        product_id = serializer.validated_data['product_id']
        movement_type = serializer.validated_data['movement_type']
        quantity = serializer.validated_data['quantity']
        reason = serializer.validated_data['reason']
        
        try:
            product = Product.objects.get(id=product_id)
            
            # Criar registro de movimentação
            stock_movement = Stock.objects.create(
                product=product,
                quantity=quantity,
                movement_type=movement_type,
                reason=reason,
                created_by=request.user
            )
            
            # Calcular quantidade atual em estoque
            current_stock = product.stock_quantity
            
            return Response({
                'message': 'Movimentação registrada com sucesso',
                'current_stock': current_stock,
                'movement_id': stock_movement.id
            }, status=status.HTTP_200_OK)
            
        except Product.DoesNotExist:
            return Response({
                'error': 'Produto não encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



