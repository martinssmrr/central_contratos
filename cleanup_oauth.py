#!/usr/bin/env python
"""
Script para limpar aplicações sociais duplicadas do Google OAuth
"""

import os
import django
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from decouple import config

def cleanup_google_apps():
    """Remove aplicações Google duplicadas e configura apenas uma"""
    
    print("🧹 Limpando aplicações Google duplicadas...")
    print("-" * 50)
    
    # Listar todas as aplicações Google
    google_apps = SocialApp.objects.filter(provider='google')
    print(f"📊 Encontradas {google_apps.count()} aplicações Google")
    
    if google_apps.count() > 1:
        print("⚠️  Múltiplas aplicações encontradas - removendo duplicatas...")
        
        # Manter apenas a primeira e remover as outras
        apps_to_delete = google_apps[1:]
        for app in apps_to_delete:
            print(f"🗑️  Removendo aplicação: {app.name} (ID: {app.id})")
            app.delete()
        
        print(f"✅ {len(apps_to_delete)} aplicação(ões) duplicada(s) removida(s)")
    
    # Verificar se ainda temos pelo menos uma aplicação
    remaining_apps = SocialApp.objects.filter(provider='google')
    
    if remaining_apps.count() == 0:
        print("📝 Nenhuma aplicação Google encontrada - criando nova...")
        create_google_app()
    else:
        print(f"✅ Aplicação Google única mantida: {remaining_apps.first().name}")
        update_existing_app(remaining_apps.first())
    
    return True

def create_google_app():
    """Cria uma nova aplicação Google"""
    client_id = config('GOOGLE_CLIENT_ID', default='')
    client_secret = config('GOOGLE_CLIENT_SECRET', default='')
    
    if not client_id or not client_secret:
        print("❌ Erro: Credenciais do Google não encontradas no .env")
        return False
    
    # Criar aplicação
    google_app = SocialApp.objects.create(
        provider='google',
        name='Google OAuth',
        client_id=client_id,
        secret=client_secret,
    )
    
    # Associar ao site
    site = Site.objects.get(id=1)
    google_app.sites.add(site)
    google_app.save()
    
    print(f"✅ Nova aplicação Google criada: {google_app.name}")
    return True

def update_existing_app(app):
    """Atualiza a aplicação existente com as credenciais do .env"""
    client_id = config('GOOGLE_CLIENT_ID', default='')
    client_secret = config('GOOGLE_CLIENT_SECRET', default='')
    
    if client_id and client_secret:
        app.client_id = client_id
        app.secret = client_secret
        app.save()
        print(f"✅ Aplicação atualizada com novas credenciais")
    
    # Garantir que está associada ao site
    site = Site.objects.get(id=1)
    if site not in app.sites.all():
        app.sites.add(site)
        app.save()
        print(f"✅ Aplicação associada ao site: {site.domain}")

if __name__ == '__main__':
    print("🔧 LIMPEZA DE APLICAÇÕES GOOGLE OAUTH")
    print("=" * 50)
    
    try:
        success = cleanup_google_apps()
        if success:
            print("-" * 50)
            print("✅ Limpeza concluída com sucesso!")
            print("🔗 Teste novamente: http://127.0.0.1:8000/users/login/")
        else:
            print("-" * 50)
            print("❌ Limpeza falhou. Verifique o arquivo .env")
    except Exception as e:
        print(f"❌ Erro durante a limpeza: {str(e)}")
        print("💡 Tente executar: python manage.py shell")
