"""
Teste completo da integração com Mercado Pago
Este script testa todo o fluxo de pagamento do sistema
"""

import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth import get_user_model
from contracts.models import Category, ContractType, Contract, Payment
from contracts.mercado_pago import MercadoPagoService
from django.urls import reverse
from django.test import Client

User = get_user_model()

def test_mercado_pago_integration():
    """Testa a integração completa com Mercado Pago"""
    
    print("🚀 Iniciando teste da integração Mercado Pago...")
    
    # 1. Verificar se o usuário de teste existe
    user, created = User.objects.get_or_create(
        username='test_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Usuário',
            'last_name': 'Teste'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print("✅ Usuário de teste criado")
    else:
        print("✅ Usuário de teste já existe")
    
    # 2. Verificar categoria e tipo de contrato (usar existentes)
    try:
        category = Category.objects.filter(is_active=True).first()
        if not category:
            category = Category.objects.create(
                name='Teste MP',
                slug='teste-mp',
                description='Categoria para teste Mercado Pago',
                icon='fas fa-test',
                is_active=True
            )
        print(f"✅ Categoria encontrada: {category.name}")
        
        contract_type = ContractType.objects.filter(category=category, is_active=True).first()
        if not contract_type:
            contract_type = ContractType.objects.create(
                name='Contrato Teste MP',
                slug='teste-mp-contrato',
                category=category,
                description='Contrato para teste Mercado Pago',
                price=29.90,
                is_active=True
            )
        print(f"✅ Tipo de contrato encontrado: {contract_type.name}")
        
    except Exception as e:
        print(f"❌ Erro ao configurar categoria/tipo: {str(e)}")
        return False
    
    # 3. Criar contrato de teste
    contract = Contract.objects.create(
        user=user,
        contract_type=contract_type,
        status='pending',
        parte1_nome='João Silva Prestador',
        parte1_cpf_cnpj='123.456.789-00',
        parte1_endereco='Rua A, 123, Centro, São Paulo - SP',
        parte2_nome='Maria Santos Tomadora',
        parte2_cpf_cnpj='987.654.321-00',
        parte2_endereco='Rua B, 456, Jardins, São Paulo - SP',
        objeto_contrato='Desenvolvimento de website completo',
        valor=2500.00,
        forma_pagamento='À vista via transferência bancária',
        data_inicio='2025-01-01',
        prazo_vigencia='30 dias',
        dados_especificos={
            'servico_descricao': 'Desenvolvimento de website responsivo',
            'prazo_execucao': '30 dias',
            'observacoes': 'Inclui hospedagem por 1 ano'
        }
    )
    print(f"✅ Contrato criado: ID {contract.id}")
    
    # 4. Criar pagamento
    payment = Payment.objects.create(
        contract=contract,
        amount=contract_type.price,
        status='pending'
    )
    print(f"✅ Pagamento criado: ID {payment.id}")
    
    # 5. Testar serviço Mercado Pago
    mp_service = MercadoPagoService()
    
    print("🔧 Testando criação de preferência no Mercado Pago...")
    try:
        preference_response = mp_service.create_preference(payment)
        
        if preference_response.get('response'):
            preference_data = preference_response['response']
            preference_id = preference_data.get('id')
            init_point = preference_data.get('init_point')
            
            print(f"✅ Preferência criada com sucesso!")
            print(f"   - ID da Preferência: {preference_id}")
            print(f"   - Link de Pagamento: {init_point}")
            
            # Atualizar pagamento com dados do MP
            payment.preference_id = preference_id
            payment.save()
            
        else:
            print("❌ Erro ao criar preferência no Mercado Pago")
            print(f"   Resposta: {preference_response}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no serviço Mercado Pago: {str(e)}")
        return False
    
    # 6. Testar URLs
    client = Client()
    client.force_login(user)
    
    print("🌐 Testando URLs do sistema...")
    
    # Testar página de detalhes do contrato
    detail_url = reverse('contracts:contract_detail', args=[contract.id])
    response = client.get(detail_url)
    if response.status_code == 200:
        print(f"✅ Página de detalhes: {detail_url}")
    else:
        print(f"❌ Erro na página de detalhes: {response.status_code}")
    
    # Testar criação de pagamento
    create_payment_url = reverse('contracts:create_payment', args=[contract.id])
    response = client.get(create_payment_url)
    if response.status_code == 302:  # Redirect para MP
        print(f"✅ Criação de pagamento: {create_payment_url}")
    else:
        print(f"❌ Erro na criação de pagamento: {response.status_code}")
    
    # Testar verificação de status
    status_url = reverse('contracts:payment_status_check', args=[contract.id])
    response = client.get(status_url)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Verificação de status: {status_url}")
        print(f"   Status: {data.get('status')}")
        print(f"   Pago: {data.get('is_paid')}")
    else:
        print(f"❌ Erro na verificação de status: {response.status_code}")
    
    # 7. Simular webhook (dados fictícios)
    print("🔔 Testando processamento de webhook...")
    webhook_data = {
        'action': 'payment.updated',
        'data': {
            'id': '12345678'  # ID fictício
        }
    }
    
    webhook_url = reverse('contracts:payment_webhook')
    response = client.post(webhook_url, webhook_data, content_type='application/json')
    print(f"✅ Webhook processado: Status {response.status_code}")
    
    print("\n🎉 Teste da integração Mercado Pago concluído!")
    print("\n📋 Resumo:")
    print(f"   - Usuário: {user.username}")
    print(f"   - Contrato: #{contract.id} - {contract.contract_type.name}")
    print(f"   - Pagamento: #{payment.id} - R$ {payment.amount}")
    print(f"   - Status: {payment.status}")
    print(f"   - Preferência MP: {payment.preference_id}")
    
    print("\n🔗 URLs para teste manual:")
    print(f"   - Contratos do usuário: http://127.0.0.1:8000{reverse('contracts:user_contracts')}")
    print(f"   - Detalhes do contrato: http://127.0.0.1:8000{detail_url}")
    print(f"   - Iniciar pagamento: http://127.0.0.1:8000{create_payment_url}")
    
    return True

if __name__ == "__main__":
    test_mercado_pago_integration()
