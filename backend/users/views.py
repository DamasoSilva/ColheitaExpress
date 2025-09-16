from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    UserProfileSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    Endpoint para registro de novos usuários
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Criar token de autenticação
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Usuário criado com sucesso!'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint para login de usuários
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login realizado com sucesso!'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint para logout de usuários
    """
    try:
        # Deletar o token do usuário
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout realizado com sucesso!'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'error': 'Erro ao realizar logout'
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para visualizar e atualizar perfil do usuário
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """
    Endpoint para atualizar dados do usuário
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Endpoint para alteração de senha
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Regenerar token após mudança de senha
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        
        return Response({
            'message': 'Senha alterada com sucesso!',
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para gerenciar perfil detalhado do usuário
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_data(request):
    """
    Endpoint para dados do dashboard baseado no tipo de usuário
    """
    user = request.user
    
    if user.user_type == 'admin':
        # Dados para dashboard administrativo
        from orders.models import Order
        from products.models import Product
        
        total_orders = Order.objects.count()
        total_products = Product.objects.count()
        total_customers = User.objects.filter(user_type='customer').count()
        
        dashboard_data = {
            'user_type': 'admin',
            'stats': {
                'total_orders': total_orders,
                'total_products': total_products,
                'total_customers': total_customers,
            }
        }
        
    elif user.user_type == 'customer':
        # Dados para dashboard do cliente
        from orders.models import Order
        
        user_orders = Order.objects.filter(customer=user)
        
        dashboard_data = {
            'user_type': 'customer',
            'stats': {
                'total_orders': user_orders.count(),
                'pending_orders': user_orders.filter(status='pending').count(),
                'delivered_orders': user_orders.filter(status='delivered').count(),
            }
        }
        
    elif user.user_type == 'driver':
        # Dados para dashboard do motorista
        from deliveries.models import Delivery
        
        driver_deliveries = Delivery.objects.filter(driver=user)
        
        dashboard_data = {
            'user_type': 'driver',
            'stats': {
                'total_deliveries': driver_deliveries.count(),
                'pending_deliveries': driver_deliveries.filter(status='assigned').count(),
                'completed_deliveries': driver_deliveries.filter(status='delivered').count(),
            }
        }
    
    else:
        dashboard_data = {
            'user_type': 'unknown',
            'stats': {}
        }
    
    return Response(dashboard_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    """
    Endpoint para verificar se o usuário está autenticado
    """
    return Response({
        'authenticated': True,
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)
