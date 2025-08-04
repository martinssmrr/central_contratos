#!/usr/bin/env python
"""
Script para popular o banco de dados com dados iniciais
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from contracts.models import ContractType

def create_contract_types():
    """Criar tipos de contratos padrão"""
    contract_types_data = [
        {
            'name': 'Prestação de Serviços',
            'slug': 'prestacao_servico',
            'description': 'Contrato para prestação de serviços em geral, ideal para autônomos e empresas de serviços.',
            'price': Decimal('49.90')
        },
        {
            'name': 'Locação Residencial',
            'slug': 'locacao_residencial',
            'description': 'Contrato de locação para imóveis residenciais com todas as cláusulas necessárias.',
            'price': Decimal('79.90')
        },
        {
            'name': 'Locação Comercial',
            'slug': 'locacao_comercial',
            'description': 'Contrato de locação para imóveis comerciais com cláusulas específicas para negócios.',
            'price': Decimal('89.90')
        },
        {
            'name': 'Compra e Venda',
            'slug': 'compra_venda',
            'description': 'Contrato para compra e venda de bens móveis e imóveis com garantias jurídicas.',
            'price': Decimal('69.90')
        },
        {
            'name': 'Confissão de Dívida',
            'slug': 'confissao_divida',
            'description': 'Contrato para formalização de dívidas com condições de pagamento e juros.',
            'price': Decimal('39.90')
        },
        {
            'name': 'Freelancer',
            'slug': 'freelancer',
            'description': 'Contrato específico para trabalhos freelancers com cláusulas de direitos autorais.',
            'price': Decimal('59.90')
        }
    ]
    
    for data in contract_types_data:
        contract_type, created = ContractType.objects.get_or_create(
            slug=data['slug'],
            defaults=data
        )
        if created:
            print(f"✓ Criado tipo de contrato: {contract_type.name}")
        else:
            print(f"○ Tipo de contrato já existe: {contract_type.name}")

def create_admin_user():
    """Criar usuário administrador"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@centralcontratos.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema'
        )
        print("✓ Usuário administrador criado")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("○ Usuário administrador já existe")

def create_demo_user():
    """Criar usuário de demonstração"""
    if not User.objects.filter(username='demo').exists():
        User.objects.create_user(
            username='demo',
            email='demo@centralcontratos.com',
            password='demo123',
            first_name='João',
            last_name='Silva'
        )
        print("✓ Usuário de demonstração criado")
        print("  Username: demo")
        print("  Password: demo123")
    else:
        print("○ Usuário de demonstração já existe")

def main():
    print("🚀 Populando banco de dados com dados iniciais...\n")
    
    print("📋 Criando tipos de contratos...")
    create_contract_types()
    
    print("\n👤 Criando usuários...")
    create_admin_user()
    create_demo_user()
    
    print("\n✅ Dados iniciais criados com sucesso!")
    print("\n🌐 Para acessar o sistema:")
    print("   • Execute: python manage.py runserver")
    print("   • Acesse: http://127.0.0.1:8000")
    print("   • Admin: http://127.0.0.1:8000/admin")

if __name__ == '__main__':
    main()
