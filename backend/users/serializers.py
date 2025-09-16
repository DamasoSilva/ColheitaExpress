from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'first_name', 
            'last_name', 'cpf_cnpj', 'phone', 'user_type'
        ]

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
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not user.is_active:
                raise serializers.ValidationError('Conta desativada.')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'birth_date', 'gender', 'street_address', 'city', 
            'state', 'zip_code', 'country'
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'cpf_cnpj', 
            'phone', 'user_type', 'is_active', 'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("As novas senhas não coincidem.")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value
