#!/usr/bin/env python
"""
Script para criar contratos de teste para demonstrar a página Meus Contratos
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from contracts.models import ContractType, Contract, Payment

def create_test_contracts():
    """Cria contratos de teste para demonstração"""
    
    # Verificar se existem usuários
    user = User.objects.filter(is_superuser=False).first()
    if not user:
        print("Criando usuário de teste...")
        user = User.objects.create_user(
            username='teste_user',
            email='teste@exemplo.com',
            password='teste123',
            first_name='João',
            last_name='Silva'
        )
    
    # Verificar se existem tipos de contrato
    contract_types = ContractType.objects.all()
    if not contract_types.exists():
        print("Criando tipos de contrato...")
        contract_types_data = [
            {
                'name': 'Prestação de Serviço',
                'slug': 'prestacao_servico',
                'description': 'Contrato para prestação de serviços profissionais',
                'price': Decimal('89.90')
            },
            {
                'name': 'Locação Residencial',
                'slug': 'locacao_residencial',
                'description': 'Contrato de locação para imóveis residenciais',
                'price': Decimal('129.90')
            },
            {
                'name': 'Compra e Venda',
                'slug': 'compra_venda',
                'description': 'Contrato de compra e venda de bens',
                'price': Decimal('149.90')
            },
            {
                'name': 'Freelancer',
                'slug': 'freelancer',
                'description': 'Contrato para trabalho freelancer',
                'price': Decimal('69.90')
            }
        ]
        
        for ct_data in contract_types_data:
            ContractType.objects.create(**ct_data)
        
        contract_types = ContractType.objects.all()
    
    # Criar contratos de teste
    print("Criando contratos de teste...")
    
    # Limpar contratos existentes do usuário
    Contract.objects.filter(user=user).delete()
    
    contracts_data = [
        {
            'contract_type': contract_types.get(slug='prestacao_servico'),
            'status': 'paid',
            'created_at': datetime.now() - timedelta(days=30)
        },
        {
            'contract_type': contract_types.get(slug='locacao_residencial'),
            'status': 'paid',
            'created_at': datetime.now() - timedelta(days=15)
        },
        {
            'contract_type': contract_types.get(slug='compra_venda'),
            'status': 'pending',
            'created_at': datetime.now() - timedelta(days=5)
        },
        {
            'contract_type': contract_types.get(slug='freelancer'),
            'status': 'pending',
            'created_at': datetime.now() - timedelta(days=2)
        },
        {
            'contract_type': contract_types.get(slug='prestacao_servico'),
            'status': 'cancelled',
            'created_at': datetime.now() - timedelta(days=45)
        }
    ]
    
    for contract_data in contracts_data:
        contract = Contract.objects.create(
            user=user,
            contract_type=contract_data['contract_type'],
            status=contract_data['status'],
            # Dados das partes
            parte1_nome=f"{user.first_name} {user.last_name}",
            parte1_cpf_cnpj="123.456.789-00",
            parte1_endereco="Rua das Flores, 123, Centro, São Paulo/SP",
            parte2_nome="Empresa Exemplo Ltda",
            parte2_cpf_cnpj="12.345.678/0001-90",
            parte2_endereco="Av. Principal, 456, Comercial, São Paulo/SP",
            # Dados do contrato
            objeto_contrato=f"Prestação de serviços de {contract_data['contract_type'].name.lower()}",
            valor=contract_data['contract_type'].price,
            forma_pagamento="À vista",
            data_inicio=contract_data['created_at'].date(),
            data_fim=(contract_data['created_at'] + timedelta(days=365)).date(),
            prazo_vigencia="12 meses",
        )
        contract.created_at = contract_data['created_at']
        contract.save()
        
        # Criar pagamento para contratos pagos
        if contract.status == 'paid':
            Payment.objects.create(
                contract=contract,
                amount=contract.contract_type.price,
                status='approved',
                payment_method='credit_card',
                transaction_id=f"txn_{contract.id}_{int(datetime.now().timestamp())}",
                payment_date=contract_data['created_at']
            )
    
    print(f"✅ Criados {len(contracts_data)} contratos de teste para o usuário {user.username}")
    print(f"👤 Usuário: {user.username}")
    print(f"🔑 Senha: teste123")
    print("\nVocê pode fazer login e acessar /contracts/my-contracts/ para ver os contratos!")

if __name__ == '__main__':
    create_test_contracts()
