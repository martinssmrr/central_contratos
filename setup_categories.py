#!/usr/bin/env python
"""
Script para popular categorias e atualizar tipos de contrato
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from contracts.models import Category, ContractType

def create_categories():
    """Cria categorias padrão"""
    categories_data = [
        {
            'name': 'Locação',
            'slug': 'locacao',
            'description': 'Contratos para locação de imóveis residenciais e comerciais',
            'icon': 'fas fa-home',
            'color': '#4CAF50',
            'order': 1
        },
        {
            'name': 'Compra e Venda',
            'slug': 'compra-venda',
            'description': 'Contratos para compra e venda de imóveis e bens',
            'icon': 'fas fa-exchange-alt',
            'color': '#2196F3',
            'order': 2
        },
        {
            'name': 'Prestação de Serviços',
            'slug': 'prestacao-servicos',
            'description': 'Contratos para prestação de serviços diversos',
            'icon': 'fas fa-handshake',
            'color': '#FF9800',
            'order': 3
        },
        {
            'name': 'Freelancer',
            'slug': 'freelancer',
            'description': 'Contratos para trabalho freelancer e consultoria',
            'icon': 'fas fa-laptop-code',
            'color': '#9C27B0',
            'order': 4
        },
        {
            'name': 'Financeiro',
            'slug': 'financeiro',
            'description': 'Contratos financeiros e confissão de dívidas',
            'icon': 'fas fa-file-invoice-dollar',
            'color': '#F44336',
            'order': 5
        }
    ]
    
    print("🏗️  Criando categorias...")
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        
        if created:
            print(f"   ✅ Categoria criada: {category.name}")
        else:
            print(f"   ℹ️  Categoria já existe: {category.name}")
    
    return Category.objects.all()

def assign_categories_to_contracts():
    """Atribui categorias aos tipos de contrato existentes"""
    print("\n🔗 Atribuindo categorias aos tipos de contrato...")
    
    # Mapeamento de slugs para categorias
    category_mapping = {
        'locacao-residencial': 'locacao',
        'locacao-comercial': 'locacao',
        'compra-venda': 'compra-venda',
        'prestacao-servico': 'prestacao-servicos',
        'prestacao_servico': 'prestacao-servicos',
        'freelancer': 'freelancer',
        'confissao-divida': 'financeiro',
        'confissao-de-dividas': 'financeiro',
    }
    
    # Obter todas as categorias
    categories = {cat.slug: cat for cat in Category.objects.all()}
    
    # Atualizar tipos de contrato
    for contract_type in ContractType.objects.all():
        category_slug = category_mapping.get(contract_type.slug)
        
        if category_slug and category_slug in categories:
            contract_type.category = categories[category_slug]
            contract_type.save()
            print(f"   ✅ {contract_type.name} → {categories[category_slug].name}")
        else:
            print(f"   ⚠️  {contract_type.name} → Sem categoria definida")

def create_sample_contracts_if_needed():
    """Cria alguns tipos de contrato de exemplo se não existirem"""
    
    if ContractType.objects.count() < 3:
        print("\n📋 Criando tipos de contrato de exemplo...")
        
        categories = {cat.slug: cat for cat in Category.objects.all()}
        
        sample_contracts = [
            {
                'name': 'Contrato de Locação Residencial',
                'slug': 'locacao-residencial',
                'description': 'Contrato para locação de imóveis residenciais com todas as cláusulas necessárias.',
                'price': 49.90,
                'category': categories.get('locacao'),
                'icon': 'fas fa-home',
                'color': '#4CAF50'
            },
            {
                'name': 'Contrato de Compra e Venda de Imóvel',
                'slug': 'compra-venda-imovel',
                'description': 'Contrato completo para compra e venda de imóveis.',
                'price': 89.90,
                'category': categories.get('compra-venda'),
                'icon': 'fas fa-exchange-alt',
                'color': '#2196F3'
            },
            {
                'name': 'Contrato de Prestação de Serviços',
                'slug': 'prestacao-servicos',
                'description': 'Contrato para prestação de serviços profissionais.',
                'price': 39.90,
                'category': categories.get('prestacao-servicos'),
                'icon': 'fas fa-handshake',
                'color': '#FF9800'
            }
        ]
        
        for contract_data in sample_contracts:
            contract, created = ContractType.objects.get_or_create(
                slug=contract_data['slug'],
                defaults=contract_data
            )
            
            if created:
                print(f"   ✅ Contrato criado: {contract.name}")

def main():
    print("🚀 Configurando sistema de categorias...")
    print("=" * 50)
    
    # 1. Criar categorias
    categories = create_categories()
    
    # 2. Atribuir categorias aos contratos existentes
    assign_categories_to_contracts()
    
    # 3. Criar contratos de exemplo se necessário
    create_sample_contracts_if_needed()
    
    print("\n" + "=" * 50)
    print("✅ Sistema de categorias configurado com sucesso!")
    
    print(f"\n📊 Resumo:")
    print(f"   - Categorias: {Category.objects.count()}")
    print(f"   - Tipos de Contrato: {ContractType.objects.count()}")
    
    print(f"\n🏷️  Categorias criadas:")
    for category in Category.objects.all():
        count = category.get_contracts_count()
        print(f"   - {category.name}: {count} contrato(s)")
    
    print(f"\n🌐 URLs disponíveis:")
    print(f"   - Catálogo geral: /contracts/catalog/")
    for category in categories:
        print(f"   - {category.name}: /contracts/catalog/categoria/{category.slug}/")

if __name__ == "__main__":
    main()
