from rest_framework import status, generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Delivery, DeliveryStatusHistory
from .serializers import (
    DeliveryListSerializer,
    DeliveryDetailSerializer,
    DeliveryCreateSerializer,
    DeliveryUpdateSerializer,
    DeliveryDriverSerializer,
    DeliveryStatusUpdateSerializer,
    DeliveryStatusHistorySerializer,
    DeliveryStatusHistoryCreateSerializer,
    DeliveryReportSerializer,
    DeliverySearchSerializer
)


class DeliveryListView(generics.ListAPIView):
    """
    Listar entregas com filtros
    """
    serializer_class = DeliveryListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tracking_code', 'order__customer__full_name', 'delivery_address']
    ordering_fields = ['created_at', 'estimated_delivery', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Delivery.objects.select_related('order__customer', 'driver')
        
        # Filtrar baseado no tipo de usuário
        if user.user_type == 'admin':
            # Admin vê todas as entregas
            pass
        elif user.user_type == 'driver':
            # Motorista vê apenas suas entregas
            queryset = queryset.filter(driver=user)
        elif user.user_type == 'customer':
            # Cliente vê apenas suas entregas
            queryset = queryset.filter(order__customer=user)
        else:
            # Outros tipos não têm acesso
            queryset = queryset.none()
        
        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_delivery_status(request, delivery_id):
    """
    Atualizar status da entrega (motorista ou admin)
    """
    delivery = get_object_or_404(Delivery, id=delivery_id)
    user = request.user
    
    # Verificar permissões
    if user.user_type == 'driver' and delivery.driver != user:
        raise permissions.PermissionDenied("Você só pode atualizar suas próprias entregas.")
    elif user.user_type not in ['admin', 'driver']:
        raise permissions.PermissionDenied("Apenas administradores e motoristas podem atualizar status.")
    
    serializer = DeliveryStatusUpdateSerializer(
        data=request.data, 
        context={'delivery': delivery}
    )
    
    if serializer.is_valid():
        new_status = serializer.validated_data['status']
        location = serializer.validated_data.get('location', '')
        notes = serializer.validated_data.get('notes', '')
        
        # Atualizar status da entrega
        delivery.status = new_status
        
        # Se foi entregue, registrar data/hora
        if new_status == 'delivered':
            delivery.actual_delivery = timezone.now()
        
        delivery.save()
        
        # Criar registro de histórico
        DeliveryStatusHistory.objects.create(
            delivery=delivery,
            status=new_status,
            notes=notes,
            changed_by=user
        )
        
        return Response({
            'message': 'Status atualizado com sucesso',
            'new_status': new_status,
            'tracking_code': delivery.tracking_code
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def track_delivery(request, tracking_code):
    """
    Rastrear entrega pelo código (público)
    """
    try:
        delivery = Delivery.objects.get(tracking_code=tracking_code)
        status_history = DeliveryStatusHistory.objects.filter(
            delivery=delivery
        ).order_by('changed_at')
        
        data = {
            'tracking_code': delivery.tracking_code,
            'status': delivery.status,
            'estimated_delivery_date': delivery.estimated_delivery_date,
            'delivery_address': delivery.delivery_address,
            'status_history': DeliveryStatusHistorySerializer(status_history, many=True).data
        }
        
        return Response(data, status=status.HTTP_200_OK)
        
    except Delivery.DoesNotExist:
        return Response({
            'error': 'Código de rastreamento não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def driver_deliveries(request):
    """
    Listar entregas do motorista logado
    """
    if request.user.user_type != 'driver':
        raise permissions.PermissionDenied("Apenas motoristas podem acessar esta funcionalidade.")
    
    deliveries = Delivery.objects.filter(
        driver=request.user
    ).select_related('order__customer').order_by('-created_at')
    
    # Filtrar por status se especificado
    status_filter = request.query_params.get('status')
    if status_filter:
        deliveries = deliveries.filter(status=status_filter)
    
    serializer = DeliveryDriverSerializer(deliveries, many=True)
    return Response(serializer.data)
