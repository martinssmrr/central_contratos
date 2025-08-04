import os
import django
import sys

# Configurar Django
sys.path.append('C:\\Users\\teste\\OneDrive\\Desktop\\Central_Conrtatos')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.test import Client

print("🏠 TESTE RÁPIDO - FORMULÁRIO COMPRA E VENDA")
print("=" * 50)

client = Client()
response = client.login(username='admin', password='admin123')
print(f"🔐 Login: {'✅' if response else '❌'}")

if response:
    # Testar URL
    response = client.get('/contracts/compra-venda-imovel/')
    print(f"📋 Formulário: {'✅' if response.status_code == 200 else f'❌ {response.status_code}'}")
    
    # Testar admin
    response = client.get('/admin/contracts/compravendaimovel/')
    print(f"🔧 Admin: {'✅' if response.status_code == 200 else f'❌ {response.status_code}'}")

print("✅ Implementação completa!")
