from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de novos usuários.
    """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'full_name', 'cpf_cnpj', 'phone',
            'street_address', 'city', 'state', 'postal_code',
            'password', 'password_confirm', 'user_type'
        ]
        extra_kwargs = {
            'user_type': {'default': 'customer'}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuários.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Conta desativada.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil do usuário.
    """
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'birth_date', 'driver_license',
            'vehicle_plate', 'vehicle_model', 'preferred_payment_method'
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para dados do usuário.
    """
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'cpf_cnpj', 'phone',
            'street_address', 'city', 'state', 'postal_code',
            'country', 'user_type', 'is_verified', 'created_at',
            'profile'
        ]
        read_only_fields = ['id', 'created_at', 'is_verified']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de dados do usuário.
    """
    class Meta:
        model = User
        fields = [
            'full_name', 'phone', 'street_address',
            'city', 'state', 'postal_code', 'country'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer para alteração de senha.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('As novas senhas não coincidem.')
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer para solicitação de redefinição de senha.
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado.')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmação de redefinição de senha.
    """
    token = serializers.CharField()
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError('As senhas não coincidem.')
        return attrs
