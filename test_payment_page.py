#!/usr/bin/env python
"""
Teste da nova página de pagamento
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from contracts.models import Contract, ContractType, Category

def test_payment_page():
    """Testa a nova página de pagamento"""
    
    print("🚀 Testando nova página de pagamento...")
    
    # Criar cliente de teste
    client = Client()
    
    # Buscar ou criar usuário de teste
    user, created = User.objects.get_or_create(
        username='test_payment',
        defaults={
            'email': 'test@payment.com',
            'first_name': 'Teste',
            'last_name': 'Pagamento'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Login
    client.force_login(user)
    
    # Buscar um contrato existente ou criar um
    contract = Contract.objects.filter(user=user).first()
    if not contract:
        # Buscar categoria e tipo de contrato
        category = Category.objects.first()
        contract_type = ContractType.objects.first()
        
        if category and contract_type:
            contract = Contract.objects.create(
                user=user,
                contract_type=contract_type,
                status='pending',
                parte1_nome='João Silva',
                parte1_cpf_cnpj='123.456.789-00',
                parte1_endereco='Rua A, 123',
                parte2_nome='Maria Santos',
                parte2_cpf_cnpj='987.654.321-00',
                parte2_endereco='Rua B, 456',
                objeto_contrato='Teste de pagamento',
                valor=100.00,
                forma_pagamento='À vista',
                data_inicio='2025-01-01',
                prazo_vigencia='30 dias'
            )
    
    if not contract:
        print("❌ Não foi possível criar/encontrar contrato para teste")
        return False
    
    # Testar URLs
    try:
        # 1. Testar página de pagamento
        payment_url = reverse('contracts:payment_page', args=[contract.id])
        print(f"📄 Testando: {payment_url}")
        
        response = client.get(payment_url)
        if response.status_code == 200:
            print("✅ Página de pagamento carregada com sucesso")
        else:
            print(f"❌ Erro na página de pagamento: {response.status_code}")
            return False
        
        # 2. Testar processo de pagamento
        process_url = reverse('contracts:process_payment', args=[contract.id])
        print(f"💳 Testando: {process_url}")
        
        response = client.post(process_url)
        if response.status_code == 302:  # Redirect esperado
            print("✅ Redirecionamento para MP funcionando")
            print(f"   Redirecionando para: {response.url}")
        else:
            print(f"❌ Erro no processo de pagamento: {response.status_code}")
            return False
        
        # 3. Testar página de erro
        error_url = reverse('core:payment_error')
        print(f"🚫 Testando: {error_url}")
        
        response = client.get(error_url)
        if response.status_code == 200:
            print("✅ Página de erro carregada com sucesso")
        else:
            print(f"❌ Erro na página de erro: {response.status_code}")
            return False
        
        print("\n🎉 Todos os testes passaram!")
        print("\n📋 URLs disponíveis:")
        print(f"   - Página de pagamento: http://127.0.0.1:8000{payment_url}")
        print(f"   - Processar pagamento: http://127.0.0.1:8000{process_url}")
        print(f"   - Página de erro: http://127.0.0.1:8000{error_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

if __name__ == '__main__':
    test_payment_page()
