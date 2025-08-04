import os
import django
import sys
from django.test import Client

# Configurar Django
sys.path.append('C:\\Users\\teste\\OneDrive\\Desktop\\Central_Conrtatos')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

# Criar cliente de teste
client = Client()

# Fazer login
response = client.login(username='admin', password='admin123')
print(f"Login realizado: {response}")

if response:
    # Testar página CRUD
    response = client.get('/adminpanel/crud-tipos/')
    print(f"Status da página CRUD: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Página CRUD carregou com sucesso!")
        
        # Testar criação de tipo de contrato
        data = {
            'name': 'Teste API',
            'description': 'Descrição teste',
            'price': '1000.00',
            'category': 'test',
            'icon': 'fas fa-test',
            'color': '#ff0000',
            'order': '10'
        }
        
        response = client.post('/adminpanel/criar-tipo/', data)
        print(f"Status criação: {response.status_code}")
        
        if response.status_code == 302:  # Redirect após sucesso
            print("✅ Criação funcionando!")
        else:
            print(f"❌ Erro na criação: {response.content.decode()[:200]}")
    else:
        print(f"❌ Erro ao carregar página: {response.content.decode()[:500]}")

from contracts.models import ContractType
print(f"\nTipos de contrato na base: {ContractType.objects.count()}")
for ct in ContractType.objects.all()[:3]:
    print(f"  - {ct.name} (R$ {ct.price})")
