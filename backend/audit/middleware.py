import logging
import time
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import AuditLog

logger = logging.getLogger('django.security')


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware para auditoria de requisições e segurança
    """
    
    def process_request(self, request):
        request.start_time = time.time()
        
        # Log de tentativas de acesso suspeitas
        suspicious_patterns = [
            '/admin/', '/.env', '/wp-admin/', '/phpmyadmin/',
            'SELECT', 'UNION', 'DROP', 'INSERT', 'UPDATE', 'DELETE',
            '<script>', 'javascript:', 'onload=', 'onerror='
        ]
        
        path = request.get_full_path().lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in path:
                logger.warning(
                    f"Suspicious request detected: {request.method} {request.get_full_path()} "
                    f"from IP {self.get_client_ip(request)} "
                    f"User-Agent: {request.META.get('HTTP_USER_AGENT', 'Unknown')}"
                )
                break
    
    def process_response(self, request, response):
        # Calcular tempo de resposta
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log de requisições lentas (> 5 segundos)
            if duration > 5:
                logger.warning(
                    f"Slow request: {request.method} {request.get_full_path()} "
                    f"took {duration:.2f}s from IP {self.get_client_ip(request)}"
                )
        
        # Log de erros de servidor
        if response.status_code >= 500:
            logger.error(
                f"Server error: {response.status_code} for {request.method} "
                f"{request.get_full_path()} from IP {self.get_client_ip(request)}"
            )
        
        # Log de tentativas de acesso não autorizado
        elif response.status_code in [401, 403]:
            user = getattr(request, 'user', AnonymousUser())
            logger.warning(
                f"Unauthorized access attempt: {response.status_code} for "
                f"{request.method} {request.get_full_path()} "
                f"from IP {self.get_client_ip(request)} "
                f"User: {user.email if hasattr(user, 'email') else 'Anonymous'}"
            )
        
        return response
    
    def get_client_ip(self, request):
        """Obter o IP real do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para adicionar cabeçalhos de segurança
    """
    
    def process_response(self, request, response):
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none';"
        )
        
        # Outros cabeçalhos de segurança
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), '
            'payment=(), usb=(), magnetometer=(), gyroscope=()'
        )
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    Middleware simples de rate limiting
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
        super().__init__(get_response)
    
    def process_request(self, request):
        from django.http import HttpResponseTooManyRequests
        from django.core.cache import cache
        
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"
        
        # Verificar rate limit (100 requests por minuto por IP)
        current_requests = cache.get(cache_key, 0)
        if current_requests >= 100:
            logger.warning(f"Rate limit exceeded for IP {ip}")
            return HttpResponseTooManyRequests("Rate limit exceeded")
        
        # Incrementar contador
        cache.set(cache_key, current_requests + 1, 60)  # 60 segundos
        
        return None
    
    def get_client_ip(self, request):
        """Obter o IP real do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
