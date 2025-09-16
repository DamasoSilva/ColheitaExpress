from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permissão para usuários administradores.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )


class IsCustomerUser(permissions.BasePermission):
    """
    Permissão para usuários clientes.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'customer'
        )


class IsDriverUser(permissions.BasePermission):
    """
    Permissão para usuários motoristas.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'driver'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão para o proprietário do objeto ou administrador.
    """
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.user_type == 'admin':
            return True
        
        # Verificar se o objeto tem um campo 'user' ou 'customer'
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'customer'):
            return obj.customer == request.user
        
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão que permite leitura para todos os usuários autenticados,
    mas escrita apenas para administradores.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Permissões de leitura para qualquer usuário autenticado
        if request.method in permissions.READONLY_METHODS:
            return True
        
        # Permissões de escrita apenas para administradores
        return request.user.user_type == 'admin'


class IsDriverOrAdmin(permissions.BasePermission):
    """
    Permissão para motoristas ou administradores.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type in ['driver', 'admin']
        )


class CanManageDeliveries(permissions.BasePermission):
    """
    Permissão para gerenciar entregas.
    Motoristas podem gerenciar suas próprias entregas.
    Administradores podem gerenciar todas as entregas.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type in ['driver', 'admin']
        )
    
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.user_type == 'admin':
            return True
        
        # Motoristas podem acessar apenas suas próprias entregas
        if request.user.user_type == 'driver':
            return obj.driver == request.user
        
        return False


class CanManageOrders(permissions.BasePermission):
    """
    Permissão para gerenciar pedidos.
    Clientes podem gerenciar seus próprios pedidos.
    Administradores podem gerenciar todos os pedidos.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type in ['customer', 'admin']
        )
    
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.user_type == 'admin':
            return True
        
        # Clientes podem acessar apenas seus próprios pedidos
        if request.user.user_type == 'customer':
            return obj.customer == request.user
        
        return False


class CanViewProducts(permissions.BasePermission):
    """
    Permissão para visualizar produtos.
    Todos os usuários autenticados podem visualizar produtos.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanManageProducts(permissions.BasePermission):
    """
    Permissão para gerenciar produtos.
    Apenas administradores podem criar, editar ou deletar produtos.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Permissões de leitura para qualquer usuário autenticado
        if request.method in permissions.READONLY_METHODS:
            return True
        
        # Permissões de escrita apenas para administradores
        return request.user.user_type == 'admin'


class CanManageStock(permissions.BasePermission):
    """
    Permissão para gerenciar estoque.
    Apenas administradores podem gerenciar estoque.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )


class CanViewReports(permissions.BasePermission):
    """
    Permissão para visualizar relatórios.
    Apenas administradores podem visualizar relatórios.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )


class CanManageUsers(permissions.BasePermission):
    """
    Permissão para gerenciar usuários.
    Apenas administradores podem gerenciar outros usuários.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )
    
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.user_type == 'admin':
            return True
        
        # Usuários podem acessar apenas seus próprios dados
        return obj == request.user


class CanManageCoupons(permissions.BasePermission):
    """
    Permissão para gerenciar cupons.
    Apenas administradores podem gerenciar cupons.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )


class CanViewAuditLogs(permissions.BasePermission):
    """
    Permissão para visualizar logs de auditoria.
    Apenas administradores podem visualizar logs de auditoria.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'admin'
        )


class CanManageNotifications(permissions.BasePermission):
    """
    Permissão para gerenciar notificações.
    Usuários podem gerenciar suas próprias notificações.
    Administradores podem gerenciar todas as notificações.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.user_type == 'admin':
            return True
        
        # Usuários podem acessar apenas suas próprias notificações
        return obj.recipient == request.user


class CanManagePayments(permissions.BasePermission):
    """
    Permissão para gerenciar pagamentos.
    Clientes podem visualizar seus próprios pagamentos.
    Administradores podem gerenciar todos os pagamentos.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type in ['customer', 'admin']
        )
    
    def has_object_permission(self, request, view, obj):
        # Administradores têm acesso total
        if request.user.user_type == 'admin':
            return True
        
        # Clientes podem acessar apenas pagamentos de seus próprios pedidos
        if request.user.user_type == 'customer':
            return obj.order.customer == request.user
        
        return False

