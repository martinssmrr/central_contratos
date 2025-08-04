#!/usr/bin/env python
"""
Script para configurar automaticamente a aplicação social do Google no Django Admin.
Execute este script após configurar as variáveis de ambiente no arquivo .env
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

def setup_google_oauth():
    """Configura automaticamente o Google OAuth no Django"""
    
    # Configurar Site
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': '127.0.0.1:8000',
            'name': 'Central de Contratos'
        }
    )
    
    if not created:
        site.domain = '127.0.0.1:8000'
        site.name = 'Central de Contratos'
        site.save()
        print(f"✅ Site atualizado: {site.name} ({site.domain})")
    else:
        print(f"✅ Site criado: {site.name} ({site.domain})")
    
    # Obter credenciais do Google
    client_id = config('GOOGLE_CLIENT_ID', default='')
    client_secret = config('GOOGLE_CLIENT_SECRET', default='')
    
    if not client_id or not client_secret:
        print("❌ Erro: GOOGLE_CLIENT_ID e GOOGLE_CLIENT_SECRET devem estar configurados no arquivo .env")
        print("📝 Edite o arquivo .env e adicione suas credenciais do Google Cloud Console")
        return False
    
    # Configurar aplicação social do Google
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google OAuth',
            'client_id': client_id,
            'secret': client_secret,
        }
    )
    
    if not created:
        google_app.client_id = client_id
        google_app.secret = client_secret
        google_app.save()
        print("✅ Aplicação Google OAuth atualizada")
    else:
        print("✅ Aplicação Google OAuth criada")
    
    # Associar o site à aplicação
    google_app.sites.add(site)
    google_app.save()
    
    print(f"✅ Configuração completa!")
    print(f"🌐 Site: {site.domain}")
    print(f"🔑 Client ID: {client_id[:20]}...")
    print(f"📄 Aplicação: {google_app.name}")
    
    return True

if __name__ == '__main__':
    print("🚀 Configurando Google OAuth...")
    print("-" * 50)
    
    try:
        success = setup_google_oauth()
        if success:
            print("-" * 50)
            print("✅ Configuração concluída com sucesso!")
            print("🔗 Acesse: http://127.0.0.1:8000/users/login/")
            print("📋 Para testar, clique em 'Continuar com Google'")
        else:
            print("-" * 50)
            print("❌ Configuração falhou. Verifique o arquivo .env")
    except Exception as e:
        print(f"❌ Erro durante a configuração: {str(e)}")
        print("💡 Verifique se o servidor Django está rodando e as migrações foram aplicadas")
