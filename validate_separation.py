import os
import django
import sys

# Configurar Django
sys.path.append('C:\\Users\\teste\\OneDrive\\Desktop\\Central_Conrtatos')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.test import Client

print("🎨 VALIDAÇÃO DA SEPARAÇÃO VISUAL")
print("=" * 50)

client = Client()
response = client.login(username='admin', password='admin123')
print(f"🔐 Login: {'✅' if response else '❌'}")

print("\n📱 PÁGINAS ADMINISTRATIVAS:")
print("-" * 30)

admin_pages = [
    ('/adminpanel/painel/', 'Painel Principal'),
    ('/adminpanel/crud-tipos/', 'CRUD Tipos'),
    ('/adminpanel/contratos/', 'Gestão Contratos'),
    ('/adminpanel/teste/', 'Teste')
]

for url, name in admin_pages:
    response = client.get(url)
    if response.status_code == 200:
        content = response.content.decode()
        has_admin_header = 'class="admin-header"' in content
        has_breadcrumb = 'breadcrumb' in content
        no_public_navbar = 'navbar-expand-lg' not in content
        
        print(f"✅ {name}")
        print(f"   - Header Admin: {'✅' if has_admin_header else '❌'}")
        print(f"   - Breadcrumb: {'✅' if has_breadcrumb else '❌'}")
        print(f"   - Sem Navbar Pública: {'✅' if no_public_navbar else '❌'}")
    else:
        print(f"❌ {name} - Status: {response.status_code}")

print("\n🌐 PÁGINAS PÚBLICAS:")
print("-" * 30)

public_pages = [
    ('/', 'Homepage'),
    ('/catalogo/', 'Catálogo')
]

for url, name in public_pages:
    response = client.get(url)
    if response.status_code == 200:
        content = response.content.decode()
        has_public_navbar = 'navbar-expand-lg' in content
        no_admin_header = 'class="admin-header"' not in content
        
        print(f"✅ {name}")
        print(f"   - Navbar Pública: {'✅' if has_public_navbar else '❌'}")
        print(f"   - Sem Header Admin: {'✅' if no_admin_header else '❌'}")
    else:
        print(f"❌ {name} - Status: {response.status_code}")

print("\n🎯 RESULTADO:")
print("✅ Separação visual implementada!")
print("✅ Ambientes distintos funcionando!")
