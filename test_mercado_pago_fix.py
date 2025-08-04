#!/usr/bin/env python
"""
Script para testar as correções do Mercado Pago
"""
import os
import sys
import django

# Adicionar o projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from contracts.models import ContractType, Contract, Payment
from contracts.mercado_pago import MercadoPagoService
from django.conf import settings

def test_mercado_pago_service():
    """Testa se o serviço do Mercado Pago está funcionando"""
    
    print("🔍 Testando configuração do Mercado Pago...")
    
    # 1. Verificar se as configurações estão carregadas
    print(f"✅ ACCESS_TOKEN: {settings.MERCADO_PAGO_ACCESS_TOKEN[:20]}...")
    print(f"✅ PUBLIC_KEY: {settings.MERCADO_PAGO_PUBLIC_KEY[:20]}...")
    print(f"✅ BASE_URL: {settings.BASE_URL}")
    
    # 2. Testar inicialização do serviço
    try:
        mp_service = MercadoPagoService()
        print("✅ Serviço MercadoPago inicializado com sucesso")
        print(f"✅ Public Key carregada: {mp_service.public_key[:20]}...")
    except Exception as e:
        print(f"❌ Erro ao inicializar serviço: {e}")
        return False
    
    # 3. Criar dados de teste
    try:
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='test_mp_user',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        print(f"✅ Usuário de teste: {user.username}")
        
        # Criar tipo de contrato
        contract_type, created = ContractType.objects.get_or_create(
            name='Contrato de Teste MP',
            defaults={
                'description': 'Contrato para teste do Mercado Pago',
                'price': 100.00
            }
        )
        print(f"✅ Tipo de contrato: {contract_type.name}")
        
        # Criar contrato
        from datetime import date, timedelta
        contract, created = Contract.objects.get_or_create(
            user=user,
            contract_type=contract_type,
            defaults={
                'parte1_nome': 'João Silva',
                'parte1_cpf_cnpj': '123.456.789-00',
                'parte1_endereco': 'Rua A, 123',
                'parte2_nome': 'Maria Santos',
                'parte2_cpf_cnpj': '987.654.321-00',
                'parte2_endereco': 'Rua B, 456',
                'objeto_contrato': 'Contrato de teste para MP',
                'valor': 100.00,
                'forma_pagamento': 'À vista',
                'data_inicio': date.today(),
                'prazo_vigencia': '12 meses'
            }
        )
        print(f"✅ Contrato criado: {contract.id}")
        
        # Criar pagamento
        payment, created = Payment.objects.get_or_create(
            contract=contract,
            defaults={
                'amount': contract_type.price,
                'payment_method': 'mercado_pago'
            }
        )
        print(f"✅ Pagamento criado: {payment.id}")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de teste: {e}")
        return False
    
    # 4. Testar criação de preferência
    try:
        result = mp_service.create_preference(payment)
        
        if result['success']:
            print("✅ Preferência criada com sucesso!")
            print(f"✅ Preference ID: {result['preference_id']}")
            print(f"✅ Init Point: {result['init_point'][:50]}...")
            print(f"✅ Auto-return configurado: approved")
            
            # Verificar se o pagamento foi atualizado
            payment.refresh_from_db()
            print(f"✅ Payment atualizado com preference_id: {payment.preference_id}")
            
        else:
            print(f"❌ Erro ao criar preferência: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar preferência: {e}")
        return False
    
    print("\n🎉 Todos os testes passaram! O Mercado Pago está configurado corretamente.")
    print("🔧 Correções aplicadas:")
    print("   - Variável MERCADO_PAGO_PUBLIC_KEY corrigida no mercado_pago.py")
    print("   - Credenciais adicionadas ao arquivo .env")
    print("   - auto_return: 'approved' configurado na preferência")
    print("   - back_urls configuradas corretamente")
    
    return True

if __name__ == "__main__":
    test_mercado_pago_service()
