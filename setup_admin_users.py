"""
Script para configurar usuários administrativos
Converte usuários staff existentes para o novo sistema de tipos
"""

import os
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

def setup_admin_users():
    """Configura usuários administrativos"""
    
    print("🔧 CONFIGURANDO USUÁRIOS ADMINISTRATIVOS...")
    print("=" * 50)
    
    # Buscar usuários staff
    staff_users = User.objects.filter(is_staff=True)
    
    print(f"📊 Usuários staff encontrados: {staff_users.count()}")
    
    admin_count = 0
    
    for user in staff_users:
        try:
            # Buscar ou criar perfil
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'admin'}
            )
            
            # Se perfil já existia, atualizar tipo
            if not created and profile.user_type != 'admin':
                profile.user_type = 'admin'
                profile.save()
                print(f"✅ {user.username}: Convertido para admin")
            elif created:
                print(f"✅ {user.username}: Perfil admin criado")
            else:
                print(f"ℹ️  {user.username}: Já é admin")
            
            admin_count += 1
            
        except Exception as e:
            print(f"❌ Erro ao configurar {user.username}: {e}")
    
    # Verificar usuários regulares
    regular_users = User.objects.filter(is_staff=False)
    client_count = 0
    
    for user in regular_users:
        try:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'user_type': 'client'}
            )
            
            if not created and profile.user_type != 'client':
                profile.user_type = 'client'
                profile.save()
                print(f"👤 {user.username}: Configurado como cliente")
            elif created:
                print(f"👤 {user.username}: Perfil cliente criado")
            
            client_count += 1
            
        except Exception as e:
            print(f"❌ Erro ao configurar {user.username}: {e}")
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DA CONFIGURAÇÃO:")
    print(f"   🛡️  Administradores: {admin_count}")
    print(f"   👥 Clientes: {client_count}")
    print(f"   📊 Total de usuários: {admin_count + client_count}")
    
    # Listar administradores
    print("\n🛡️  USUÁRIOS ADMINISTRATIVOS:")
    admin_profiles = UserProfile.objects.filter(user_type='admin')
    for profile in admin_profiles:
        user = profile.user
        print(f"   • {user.username} ({user.email or 'sem email'})")
        print(f"     - Staff: {user.is_staff}")
        print(f"     - Superuser: {user.is_superuser}")
        print(f"     - Ativo: {user.is_active}")
    
    print("\n✅ CONFIGURAÇÃO CONCLUÍDA!")
    return True

if __name__ == "__main__":
    try:
        setup_admin_users()
    except Exception as e:
        print(f"❌ ERRO DURANTE A CONFIGURAÇÃO: {e}")
        import traceback
        traceback.print_exc()
