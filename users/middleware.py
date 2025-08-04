"""
Middleware para controle de acesso administrativo
Separa usuários admin dos clientes comuns
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from users.models import UserProfile


class AdminAccessMiddleware:
    """
    Middleware para controlar acesso entre admin e front-end
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Processa a view antes dela ser executada
        """
        
        # URLs que não precisam de controle
        exempt_paths = [
            '/admin/login/',
            '/painel-admin/',
            '/login/',
            '/logout/', 
            '/register/',
            '/static/',
            '/media/',
            '/accounts/',
            '/__debug__/',
        ]
        
        # URLs do painel admin
        admin_paths = [
            '/adminpanel/',
        ]
        
        # URLs do front-end (catálogo, checkout, etc.)
        frontend_paths = [
            '/contracts/',
            '/profile/',
            '/checkout/',
            '/catalog/',
        ]
        
        path = request.path
        
        # Ignorar URLs isentas
        if any(path.startswith(exempt_path) for exempt_path in exempt_paths):
            return None
            
        # Se usuário não está logado, permitir acesso normal
        if not request.user.is_authenticated:
            return None
            
        try:
            user_profile = request.user.userprofile
        except:
            # Criar perfil se não existir
            user_profile = UserProfile.objects.create(user=request.user)
        
        # Verificar se é admin tentando acessar front-end
        if user_profile.is_admin():
            if any(path.startswith(frontend_path) for frontend_path in frontend_paths):
                messages.warning(
                    request, 
                    'Usuários administrativos não têm acesso ao front-end. Redirecionando para o painel admin.'
                )
                return redirect('adminpanel:admin_panel')
        
        # Verificar se é cliente tentando acessar painel admin
        elif user_profile.is_client():
            if any(path.startswith(admin_path) for admin_path in admin_paths):
                messages.error(
                    request, 
                    'Você não tem permissão para acessar o painel administrativo.'
                )
                return redirect('core:home')
        
        return None


class AdminLoginRedirectMiddleware:
    """
    Middleware para redirecionar usuários admin após login
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se usuário acabou de fazer login
        if (request.user.is_authenticated and 
            hasattr(request, 'session') and 
            request.session.get('just_logged_in')):
            
            try:
                user_profile = request.user.userprofile
                
                # Se é admin, redirecionar para painel
                if user_profile.is_admin():
                    request.session.pop('just_logged_in', None)
                    return redirect('adminpanel:admin_panel')
                    
            except:
                pass
            
            # Remover flag após verificação
            request.session.pop('just_logged_in', None)
        
        response = self.get_response(request)
        return response
