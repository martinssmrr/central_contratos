import os
import django
import sys

# Configurar Django
sys.path.append('C:\\Users\\teste\\OneDrive\\Desktop\\Central_Conrtatos')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.test import Client

# Criar cliente de teste
client = Client()

# Fazer login
response = client.login(username='admin', password='admin123')
print(f"Login realizado: {response}")

if response:
    # Testar páginas administrativas
    pages = [
        ('/adminpanel/teste/', 'Página de Teste'),
        ('/adminpanel/painel/', 'Painel Admin'),
        ('/adminpanel/crud-tipos/', 'CRUD Tipos'),
        ('/adminpanel/contratos/', 'Gestão de Contratos')
    ]
    
    for url, name in pages:
        try:
            response = client.get(url)
            status = "✅ OK" if response.status_code == 200 else f"❌ Erro {response.status_code}"
            print(f"{name}: {status}")
        except Exception as e:
            print(f"{name}: ❌ Erro: {str(e)}")

    # Testar página do front-end para comparar
    response = client.get('/')
    status = "✅ OK" if response.status_code == 200 else f"❌ Erro {response.status_code}"
    print(f"Homepage Front-end: {status}")

else:
    print("❌ Falha no login")
