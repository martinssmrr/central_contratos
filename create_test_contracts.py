#!/usr/bin/env python
"""
Script para criar contratos de teste para demonstrar a página de perfil
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from contracts.models import ContractType, Contract
from users.models import UserProfile

def create_test_contracts():
    """Cria contratos de teste para o usuário demo"""
    
    # Buscar usuário demo
    try:
        demo_user = User.objects.get(username='demo')
        print(f"✅ Usuário demo encontrado: {demo_user.email}")
    except User.DoesNotExist:
        print("❌ Usuário demo não encontrado. Criando...")
        demo_user = User.objects.create_user(
            username='demo',
            email='demo@centraldecontratos.com',
            password='demo123',
            first_name='João',
            last_name='Silva'
        )
        print(f"✅ Usuário demo criado: {demo_user.email}")
    
    # Garantir que o perfil existe
    profile, created = UserProfile.objects.get_or_create(
        user=demo_user,
        defaults={
            'phone': '(11) 99999-9999',
            'cpf_cnpj': '123.456.789-00',
            'address': 'Rua das Flores, 123, São Paulo - SP'
        }
    )
    
    if created:
        print("✅ Perfil do usuário demo criado")
    
    # Buscar tipos de contratos
    contract_types = ContractType.objects.all()
    if not contract_types.exists():
        print("❌ Nenhum tipo de contrato encontrado")
        return
    
    print(f"📋 Encontrados {contract_types.count()} tipos de contratos")
    
    # Criar contratos de teste
    test_contracts = [
        {
            'contract_type': contract_types.filter(name__icontains='prestação').first(),
            'status': 'paid',
            'created_days_ago': 30
        },
        {
            'contract_type': contract_types.filter(name__icontains='locação').first(),
            'status': 'paid',
            'created_days_ago': 15
        },
        {
            'contract_type': contract_types.filter(name__icontains='compra').first(),
            'status': 'pending',
            'created_days_ago': 5
        },
        {
            'contract_type': contract_types.filter(name__icontains='freelancer').first(),
            'status': 'pending',
            'created_days_ago': 2
        },
        {
            'contract_type': contract_types.filter(name__icontains='confissão').first(),
            'status': 'paid',
            'created_days_ago': 45
        }
    ]
    
    created_count = 0
    
    for contract_data in test_contracts:
        if contract_data['contract_type']:
            # Verificar se já existe contrato similar
            existing = Contract.objects.filter(
                user=demo_user,
                contract_type=contract_data['contract_type']
            ).first()
            
            if not existing:
                created_date = datetime.now() - timedelta(days=contract_data['created_days_ago'])
                
                contract = Contract.objects.create(
                    user=demo_user,
                    contract_type=contract_data['contract_type'],
                    status=contract_data['status'],
                    # Dados das partes
                    parte1_nome=demo_user.get_full_name() or demo_user.username,
                    parte1_cpf_cnpj='123.456.789-00',
                    parte1_endereco='Rua das Flores, 123, São Paulo - SP',
                    parte2_nome='Empresa XYZ Ltda',
                    parte2_cpf_cnpj='12.345.678/0001-90',
                    parte2_endereco='Av. Paulista, 1000, São Paulo - SP',
                    # Dados do contrato
                    objeto_contrato=f'Contrato de {contract_data["contract_type"].name}',
                    valor=contract_data['contract_type'].price,
                    forma_pagamento='À vista',
                    data_inicio=created_date.date(),
                    prazo_vigencia='12 meses',
                    dados_especificos={}
                )
                
                # Atualizar data de criação
                contract.created_at = created_date
                contract.save()
                
                print(f"✅ Contrato criado: {contract.contract_type.name} - {contract.status}")
                created_count += 1
            else:
                print(f"○ Contrato já existe: {contract_data['contract_type'].name}")
    
    print(f"\n🎉 Processo concluído!")
    print(f"📊 Contratos criados: {created_count}")
    print(f"👤 Usuário de teste: {demo_user.username}")
    print(f"🔑 Senha: demo123")
    print(f"📧 Email: {demo_user.email}")
    print(f"\n🌐 Para testar:")
    print(f"   1. Acesse: http://127.0.0.1:8000/users/login/")
    print(f"   2. Faça login com: demo / demo123")
    print(f"   3. Acesse o perfil: http://127.0.0.1:8000/users/profile/")

if __name__ == '__main__':
    create_test_contracts()
