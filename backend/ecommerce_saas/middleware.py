import time
import logging
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.conf import settings
import hashlib
import json

logger = logging.getLogger(__name__)


class CacheMiddleware(MiddlewareMixin):
    """
    Middleware de cache inteligente para otimizar performance
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        # Não cachear requisições autenticadas ou métodos que modificam dados
        if (request.user.is_authenticated or 
            request.method in ['POST', 'PUT', 'PATCH', 'DELETE'] or
            'admin' in request.path):
            return None
        
        # Gerar chave de cache baseada na URL e parâmetros
        cache_key = self._generate_cache_key(request)
        
        # Tentar obter resposta do cache
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.debug(f"Cache hit for {request.path}")
            response = HttpResponse(
                cached_response['content'],
                content_type=cached_response['content_type'],
                status=cached_response['status']
            )
            # Adicionar headers de cache
            response['X-Cache'] = 'HIT'
            response['Cache-Control'] = 'public, max-age=300'
            return response
        
        return None
    
    def process_response(self, request, response):
        # Só cachear respostas GET bem-sucedidas
        if (request.method == 'GET' and 
            response.status_code == 200 and
            not request.user.is_authenticated and
            'admin' not in request.path):
            
            cache_key = self._generate_cache_key(request)
            
            # Cachear por 5 minutos para páginas públicas
            cache_data = {
                'content': response.content.decode('utf-8'),
                'content_type': response.get('Content-Type', 'text/html'),
                'status': response.status_code
            }
            
            cache.set(cache_key, cache_data, 300)  # 5 minutos
            response['X-Cache'] = 'MISS'
            logger.debug(f"Cached response for {request.path}")
        
        return response
    
    def _generate_cache_key(self, request):
        """Gerar chave única para cache"""
        url_with_params = request.get_full_path()
        return f"page_cache:{hashlib.md5(url_with_params.encode()).hexdigest()}"


class CompressionMiddleware(MiddlewareMixin):
    """
    Middleware para compressão de respostas
    """
    
    def process_response(self, request, response):
        # Adicionar headers de compressão para arquivos estáticos
        if response.get('Content-Type', '').startswith(('text/', 'application/json', 'application/javascript')):
            response['Vary'] = 'Accept-Encoding'
        
        return response


class PerformanceMiddleware(MiddlewareMixin):
    """
    Middleware para monitoramento de performance
    """
    
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Adicionar header de tempo de resposta
            response['X-Response-Time'] = f"{duration:.3f}s"
            
            # Log de requisições lentas
            if duration > 2.0:  # Mais de 2 segundos
                logger.warning(
                    f"Slow request: {request.method} {request.get_full_path()} "
                    f"took {duration:.3f}s"
                )
            
            # Métricas para monitoramento
            if hasattr(settings, 'ENABLE_METRICS') and settings.ENABLE_METRICS:
                self._record_metrics(request, response, duration)
        
        return response
    
    def _record_metrics(self, request, response, duration):
        """Registrar métricas de performance"""
        try:
            from audit.models import SystemMetrics
            
            # Registrar tempo de resposta
            SystemMetrics.objects.create(
                metric_type='performance',
                name='response_time',
                value=duration,
                unit='seconds',
                metadata={
                    'path': request.path,
                    'method': request.method,
                    'status_code': response.status_code
                }
            )
        except Exception as e:
            logger.error(f"Error recording metrics: {e}")


class APIThrottleMiddleware(MiddlewareMixin):
    """
    Middleware de throttling específico para API
    """
    
    def process_request(self, request):
        # Aplicar throttling apenas para rotas da API
        if not request.path.startswith('/api/'):
            return None
        
        # Obter IP do cliente
        ip = self._get_client_ip(request)
        
        # Chave de throttling
        throttle_key = f"api_throttle:{ip}"
        
        # Verificar limite (100 requests por minuto para API)
        current_requests = cache.get(throttle_key, 0)
        
        if current_requests >= 100:
            logger.warning(f"API rate limit exceeded for IP {ip}")
            return HttpResponse(
                json.dumps({'error': 'Rate limit exceeded'}),
                content_type='application/json',
                status=429
            )
        
        # Incrementar contador
        cache.set(throttle_key, current_requests + 1, 60)
        
        return None
    
    def _get_client_ip(self, request):
        """Obter IP real do cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class DatabaseOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware para otimização de consultas ao banco de dados
    """
    
    def process_request(self, request):
        if settings.DEBUG:
            from django.db import connection
            request.queries_before = len(connection.queries)
    
    def process_response(self, request, response):
        if settings.DEBUG and hasattr(request, 'queries_before'):
            from django.db import connection
            
            queries_count = len(connection.queries) - request.queries_before
            
            # Log de muitas consultas
            if queries_count > 10:
                logger.warning(
                    f"High number of database queries: {queries_count} "
                    f"for {request.method} {request.get_full_path()}"
                )
            
            # Adicionar header com número de consultas
            response['X-DB-Queries'] = str(queries_count)
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para adicionar cabeçalhos de segurança
    """
    
    def process_response(self, request, response):
        # Content Security Policy
        if not response.get('Content-Security-Policy'):
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://js.stripe.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https: blob:; "
                "connect-src 'self' https: wss:; "
                "frame-src 'self' https://js.stripe.com; "
                "object-src 'none'; "
                "base-uri 'self'; "
                "form-action 'self';"
            )
            response['Content-Security-Policy'] = csp
        
        # Outros cabeçalhos de segurança
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': (
                'geolocation=(), microphone=(), camera=(), '
                'payment=(), usb=(), magnetometer=(), gyroscope=()'
            )
        }
        
        for header, value in security_headers.items():
            if not response.get(header):
                response[header] = value
        
        # HSTS apenas em HTTPS
        if request.is_secure() and not response.get('Strict-Transport-Security'):
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        return response
