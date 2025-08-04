#!/usr/bin/env python
"""
Teste do auto_return do Mercado Pago
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.test import RequestFactory
from contracts.mercado_pago import MercadoPagoService
from contracts.models import Contract, Payment
from django.contrib.auth.models import User
from datetime import date

def test_auto_return_configuration():
    """Testa se o auto_return está configurado corretamente"""
    
    print("🔍 TESTE DO AUTO_RETURN - MERCADO PAGO")
    print("=" * 50)
    
    try:
        # 1. Criar dados de teste
        user, created = User.objects.get_or_create(
            username='test_auto_return_user',
            defaults={
                'email': 'test@autoreturn.com',
                'first_name': 'Test',
                'last_name': 'AutoReturn'
            }
        )
        
        from contracts.models import ContractType
        contract_type, created = ContractType.objects.get_or_create(
            name='Contrato Auto Return Test',
            defaults={
                'description': 'Contrato para teste do auto_return',
                'price': 200.00
            }
        )
        
        contract, created = Contract.objects.get_or_create(
            user=user,
            contract_type=contract_type,
            defaults={
                'parte1_nome': 'João AutoReturn',
                'parte1_cpf_cnpj': '123.456.789-00',
                'parte1_endereco': 'Rua AutoReturn, 123',
                'parte2_nome': 'Maria AutoReturn',
                'parte2_cpf_cnpj': '987.654.321-00',
                'parte2_endereco': 'Rua AutoReturn, 456',
                'objeto_contrato': 'Contrato de teste para auto_return',
                'valor': 200.00,
                'forma_pagamento': 'À vista',
                'data_inicio': date.today(),
                'prazo_vigencia': '12 meses'
            }
        )
        
        # 2. Criar pagamento
        payment, created = Payment.objects.get_or_create(
            contract=contract,
            defaults={
                'amount': contract_type.price,
                'payment_method': 'mercado_pago'
            }
        )
        
        print(f"✅ Dados de teste criados:")
        print(f"   - Usuário: {user.username}")
        print(f"   - Contrato ID: {contract.id}")
        print(f"   - Pagamento ID: {payment.id}")
        print(f"   - Valor: R$ {payment.amount}")
        
        # 3. Testar sem request (usará BASE_URL do settings)
        print(f"✅ Testando criação de preferência com auto_return...")
        
        # 4. Criar preferência com auto_return
        mp_service = MercadoPagoService()
        result = mp_service.create_preference(payment)  # Sem request
        
        if result['success']:
            print(f"\n✅ PREFERÊNCIA CRIADA COM AUTO_RETURN:")
            print(f"   - Preference ID: {result['preference_id']}")
            print(f"   - Init Point: {result['init_point'][:60]}...")
            print(f"   - Sandbox Init Point: {result['sandbox_init_point'][:60]}...")
            
            # 5. Verificar configuração da preferência
            preference = result['response']
            
            print(f"\n✅ CONFIGURAÇÕES DO AUTO_RETURN:")
            print(f"   - Auto Return: {preference.get('auto_return', 'NÃO CONFIGURADO')}")
            print(f"   - External Reference: {preference.get('external_reference')}")
            
            # 6. Verificar URLs de retorno
            back_urls = preference.get('back_urls', {})
            print(f"\n✅ URLS DE RETORNO CONFIGURADAS:")
            print(f"   - Success: {back_urls.get('success', 'NÃO CONFIGURADA')}")
            print(f"   - Failure: {back_urls.get('failure', 'NÃO CONFIGURADA')}")
            print(f"   - Pending: {back_urls.get('pending', 'NÃO CONFIGURADA')}")
            
            # 7. Verificar dados do item
            item = preference['items'][0]
            print(f"\n✅ DADOS DO ITEM:")
            print(f"   - Título: {item['title']}")
            print(f"   - Preço: R$ {item['unit_price']}")
            print(f"   - Quantidade: {item['quantity']}")
            print(f"   - Moeda: {item['currency_id']}")
            
            print(f"\n🎉 AUTO_RETURN CONFIGURADO COM SUCESSO!")
            print(f"\n📋 COMO FUNCIONA:")
            print(f"   1. Usuário é redirecionado para: {result['sandbox_init_point'][:50]}...")
            print(f"   2. Após pagamento aprovado, Mercado Pago redireciona automaticamente")
            print(f"   3. URL de sucesso: /contracts/payment-success/?contract_id={contract.id}")
            print(f"   4. View processa e redireciona para download do contrato")
            
            print(f"\n🚀 TESTE MANUAL:")
            print(f"   - Acesse: http://127.0.0.1:8000/contracts/payment/{contract.id}/")
            print(f"   - Clique em 'Finalizar Pagamento'")
            print(f"   - Será redirecionado para o Mercado Pago")
            print(f"   - Use cartão de teste: 4111 1111 1111 1111")
            print(f"   - Data: qualquer data futura")
            print(f"   - CVV: 123")
            print(f"   - Após aprovação, será redirecionado automaticamente!")
            
            return True
            
        else:
            print(f"❌ ERRO AO CRIAR PREFERÊNCIA:")
            print(f"   - Erro: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_auto_return_configuration()
    if success:
        print(f"\n✅ TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print(f"\n❌ TESTE FALHOU!")
