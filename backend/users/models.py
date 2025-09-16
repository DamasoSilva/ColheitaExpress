from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """
    Manager customizado para o modelo User
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        
        email = self.normalize_email(email)
        # Usar o email como username também
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de usuário customizado que estende o AbstractUser do Django.
    Inclui campos específicos para o e-commerce como CPF/CNPJ, telefone e tipo de usuário.
    """
    
    USER_TYPE_CHOICES = [
        ('admin', 'Administrador'),
        ('customer', 'Cliente'),
        ('driver', 'Motorista'),
    ]
    
    # Campos básicos
    email = models.EmailField(unique=True, verbose_name='E-mail')
    full_name = models.CharField(max_length=255, verbose_name='Nome Completo')
    
    # CPF/CNPJ com validação
    cpf_cnpj_validator = RegexValidator(
        regex=r'^\d{11}$|^\d{14}$',
        message='CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'
    )
    cpf_cnpj = models.CharField(
        max_length=14,
        unique=True,
        validators=[cpf_cnpj_validator],
        verbose_name='CPF/CNPJ'
    )
    
    # Telefone
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Número de telefone deve estar no formato: "+999999999". Até 15 dígitos permitidos.'
    )
    phone = models.CharField(
        max_length=17,
        validators=[phone_validator],
        verbose_name='Telefone'
    )
    
    # Tipo de usuário
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',
        verbose_name='Tipo de Usuário'
    )
    
    # Campos de endereço
    street_address = models.CharField(max_length=255, verbose_name='Endereço')
    city = models.CharField(max_length=100, verbose_name='Cidade')
    state = models.CharField(max_length=100, verbose_name='Estado')
    postal_code = models.CharField(max_length=10, verbose_name='CEP')
    country = models.CharField(max_length=100, default='Brasil', verbose_name='País')
    
    # Campos de controle
    is_verified = models.BooleanField(default=False, verbose_name='Verificado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    # Manager customizado
    objects = UserManager()
    
    # Configurações do modelo
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'cpf_cnpj']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    @property
    def is_customer(self):
        return self.user_type == 'customer'
    
    @property
    def is_driver(self):
        return self.user_type == 'driver'
    
    def get_full_address(self):
        """Retorna o endereço completo formatado"""
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


class UserProfile(models.Model):
    """
    Perfil adicional do usuário para informações específicas por tipo.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')
    
    # Campos específicos para motoristas
    driver_license = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name='CNH'
    )
    vehicle_plate = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        verbose_name='Placa do Veículo'
    )
    vehicle_model = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name='Modelo do Veículo'
    )
    
    # Campos específicos para clientes
    preferred_payment_method = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name='Método de Pagamento Preferido'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
    
    def __str__(self):
        return f"Perfil de {self.user.full_name}"
