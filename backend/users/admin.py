from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuração do admin para o modelo User customizado.
    """
    list_display = ('email', 'full_name', 'user_type', 'is_verified', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'full_name', 'cpf_cnpj', 'phone')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {
            'fields': ('full_name', 'cpf_cnpj', 'phone', 'user_type')
        }),
        (_('Endereço'), {
            'fields': ('street_address', 'city', 'state', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Datas Importantes'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'cpf_cnpj', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo UserProfile.
    """
    list_display = ('user', 'birth_date', 'driver_license', 'vehicle_plate')
    list_filter = ('user__user_type', 'birth_date')
    search_fields = ('user__full_name', 'user__email', 'driver_license', 'vehicle_plate')
    
    fieldsets = (
        (_('Informações Gerais'), {
            'fields': ('user', 'avatar', 'birth_date')
        }),
        (_('Informações do Motorista'), {
            'fields': ('driver_license', 'vehicle_plate', 'vehicle_model'),
            'classes': ('collapse',)
        }),
        (_('Informações do Cliente'), {
            'fields': ('preferred_payment_method',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
