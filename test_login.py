import os
import django
import sys

# Configurar Django
sys.path.append('C:\\Users\\teste\\OneDrive\\Desktop\\Central_Conrtatos')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.test import Client

# Criar cliente de teste
client = Client()

# Fazer login
response = client.login(username='admin', password='admin123')
print(f"Login realizado: {response}")

if response:
    # Testar página de teste
    response = client.get('/adminpanel/teste/')
    print(f"Status da página teste: {response.status_code}")
    
    # Testar página CRUD
    response = client.get('/adminpanel/crud-tipos/')
    print(f"Status da página CRUD: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Erro: {response.content.decode()[:500]}")
