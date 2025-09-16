from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserUpdateSerializer, PasswordChangeSerializer, UserProfileSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
try:
    from audit.models import AuditLog
except ImportError:
    AuditLog = None


class UserRegistrationView(generics.CreateAPIView):
    """
    View para registro de novos usuários.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Criar perfil do usuário
        UserProfile.objects.get_or_create(user=user)
        
        # Log de auditoria
        if AuditLog:
            AuditLog.log_action(
                user=None,
                action='create',
                description=f'Novo usuário registrado: {user.email}',
                content_object=user,
                user_ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        
        # Gerar token JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuário criado com sucesso',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Endpoint para login de usuários
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Log de auditoria
        if AuditLog:
            AuditLog.log_action(
                user=user,
                action='login',
                description=f'Login realizado por {user.email}',
                user_ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        
        # Gerar token JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'Login realizado com sucesso!'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Endpoint para logout de usuários
    """
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        # Log de auditoria
        if AuditLog:
            AuditLog.log_action(
                user=request.user,
                action='logout',
                description=f'Logout realizado por {request.user.email}',
                user_ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        
        return Response({
            'message': 'Logout realizado com sucesso!'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Erro ao realizar logout'
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para visualizar e atualizar perfil do usuário
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_values = {
            'full_name': instance.full_name,
            'phone': instance.phone,
            'street_address': instance.street_address,
            'city': instance.city,
            'state': instance.state,
            'postal_code': instance.postal_code,
        }
        
        serializer = UserUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Log de auditoria
        if AuditLog:
            AuditLog.log_action(
                user=request.user,
                action='update',
                description='Perfil do usuário atualizado',
                content_object=instance,
                old_values=old_values,
                new_values=serializer.validated_data,
                user_ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        
        return Response(UserSerializer(instance).data)


class UserUpdateView(generics.UpdateAPIView):
    """
    Endpoint para atualizar dados do usuário
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    """
    Endpoint para alteração de senha
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        
        # Log de auditoria
        if AuditLog:
            AuditLog.log_action(
                user=request.user,
                action='password_change',
                description='Senha alterada pelo usuário',
                user_ip=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        
        return Response({
            'message': 'Senha alterada com sucesso!'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Endpoint para gerenciar perfil detalhado do usuário
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    """
    Endpoint para solicitação de redefinição de senha.
    """
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Gerar token de redefinição
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Enviar email (implementar com sistema de notificações)
        reset_url = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/reset-password/{uid}/{token}/"
        
        # Por enquanto, apenas retornar o link (em produção, enviar por email)
        return Response({
            'message': 'Link de redefinição enviado',
            'reset_url': reset_url  # Remover em produção
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    """
    Endpoint para confirmação de redefinição de senha.
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Decodificar UID e verificar token
            uid = force_str(urlsafe_base64_decode(request.data.get('uid')))
            user = User.objects.get(pk=uid)
            token = serializer.validated_data['token']
            
            if default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                # Log de auditoria
                if AuditLog:
                    AuditLog.log_action(
                        user=user,
                        action='password_change',
                        description='Senha redefinida via token',
                        user_ip=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT')
                    )
                
                return Response({'message': 'Senha redefinida com sucesso'})
            else:
                return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
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
@permission_classes([permissions.IsAuthenticated])
def check_auth(request):
    """
    Endpoint para verificar se o usuário está autenticado
    """
    return Response({
        'authenticated': True,
        'user': UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)
