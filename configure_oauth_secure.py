#!/usr/bin/env python
"""
Script de configuração segura do Google OAuth
Central de Contratos - Sem credenciais hardcoded
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from decouple import config

def setup_google_oauth():
    """
    Configura o Google OAuth usando credenciais do arquivo .env
    NUNCA exponha credenciais reais no código!
    """
    print("🔐 CONFIGURAÇÃO SEGURA DO GOOGLE OAUTH")
    print("=" * 50)
    
    try:
        # 1. Verificar se as credenciais estão no .env
        client_id = config('GOOGLE_CLIENT_ID', default='')
        client_secret = config('GOOGLE_CLIENT_SECRET', default='')
        
        if not client_id or not client_secret:
            print("❌ ERRO: Credenciais do Google não encontradas no arquivo .env")
            print("\n📝 INSTRUÇÕES:")
            print("1. Copie o arquivo .env.example para .env")
            print("2. Adicione suas credenciais reais do Google Cloud Console")
            print("3. Execute este script novamente")
            return False
        
        # 2. Remover configurações antigas
        SocialApp.objects.filter(provider='google').delete()
        print("✅ Configurações antigas removidas")
        
        # 3. Criar nova configuração
        app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )
        
        # 4. Associar aos sites
        sites = Site.objects.all()
        app.sites.set(sites)
        
        print("✅ Google OAuth configurado com segurança")
        print(f"🌐 Sites: {[s.domain for s in sites]}")
        print(f"🔑 Client ID: {client_id[:20]}...") # Mostra apenas parte da credencial
        
        print("\n🎯 CONFIGURAÇÃO COMPLETA!")
        print("📋 URIs de callback que devem estar no Google Cloud Console:")
        for site in sites:
            print(f"   - http://{site.domain}/accounts/google/login/callback/")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    setup_google_oauth()
