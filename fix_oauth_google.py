#!/usr/bin/env python3
"""
Script para resolver definitivamente o problema de OAuth Google
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken
from django.contrib.sites.models import Site
from django.core.management import call_command

def fix_oauth_google():
    """Corrige o problema do OAuth Google de forma definitiva"""
    
    print("🔧 CORREÇÃO DEFINITIVA DO OAUTH GOOGLE")
    print("=" * 50)
    
    try:
        # 1. Limpar completamente todos os dados OAuth
        print("🧹 Passo 1: Limpeza completa...")
        
        # Deletar tokens primeiro (dependências)
        token_count = SocialToken.objects.count()
        SocialToken.objects.all().delete()
        print(f"   ✅ Removidos {token_count} tokens")
        
        # Deletar contas sociais
        account_count = SocialAccount.objects.count()
        SocialAccount.objects.all().delete()
        print(f"   ✅ Removidas {account_count} contas sociais")
        
        # Deletar aplicações
        app_count = SocialApp.objects.count()
        SocialApp.objects.all().delete()
        print(f"   ✅ Removidas {app_count} aplicações OAuth")
        
        # 2. Verificar e corrigir sites
        print("\n🌐 Passo 2: Verificação de sites...")
        
        # Remover sites duplicados
        sites = Site.objects.all()
        if sites.count() > 1:
            # Manter apenas o primeiro
            main_site = sites.first()
            Site.objects.exclude(id=main_site.id).delete()
            print(f"   ✅ Removidos sites duplicados, mantido: {main_site.domain}")
        
        # Garantir que o site principal existe
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': '127.0.0.1:8000',
                'name': 'Central de Contratos'
            }
        )
        
        if not created:
            # Atualizar se já existe
            site.domain = '127.0.0.1:8000'
            site.name = 'Central de Contratos'
            site.save()
        
        print(f"   ✅ Site configurado: {site.domain} (ID: {site.id})")
        
        # 3. Recriar aplicação OAuth única
        print("\n🔑 Passo 3: Recriando aplicação OAuth...")
        
        # Ler credenciais do .env
        env_path = '.env'
        google_client_id = None
        google_client_secret = None
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_OAUTH_CLIENT_ID='):
                        google_client_id = line.split('=', 1)[1].strip().strip('"')
                    elif line.startswith('GOOGLE_OAUTH_CLIENT_SECRET='):
                        google_client_secret = line.split('=', 1)[1].strip().strip('"')
        
        if google_client_id and google_client_secret:
            # Criar aplicação única
            social_app = SocialApp.objects.create(
                provider='google',
                name='Google OAuth',
                client_id=google_client_id,
                secret=google_client_secret,
            )
            
            # Associar ao site
            social_app.sites.add(site)
            
            print(f"   ✅ Aplicação criada: {social_app.name}")
            print(f"   🔗 Client ID: {google_client_id[:20]}...")
            print(f"   🌐 Associada ao site: {site.domain}")
        else:
            print("   ⚠️  Credenciais Google não encontradas no .env")
            return False
        
        # 4. Verificação final
        print("\n✅ Passo 4: Verificação final...")
        
        final_apps = SocialApp.objects.filter(provider='google')
        print(f"   📊 Total de apps Google: {final_apps.count()}")
        
        if final_apps.count() == 1:
            app = final_apps.first()
            associated_sites = app.sites.all()
            print(f"   🎯 App: {app.name}")
            print(f"   🌐 Sites: {[s.domain for s in associated_sites]}")
            print("\n🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print("🔗 Teste em: http://127.0.0.1:8000/users/login/")
            return True
        else:
            print("   ❌ Erro: Múltiplas aplicações ainda existem")
            return False
            
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    success = fix_oauth_google()
    if not success:
        print("\n💡 SOLUÇÃO ALTERNATIVA:")
        print("1. Desabilite temporariamente o OAuth nos templates")
        print("2. Use apenas login/registro por formulário")
        print("3. Configure o OAuth em produção com domínio fixo")
        sys.exit(1)
    else:
        print("\n🚀 OAuth Google configurado e pronto para uso!")
        sys.exit(0)
