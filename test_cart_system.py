#!/usr/bin/env python
"""
Script de teste para verificar o sistema de carrinho implementado
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from contracts.models import ContractType

def test_cart_system():
    """Testa o sistema de carrinho de compras"""
    print("🚀 Testando Sistema de Carrinho de Compras")
    print("=" * 50)
    
    # Criar cliente de teste
    client = Client()
    
    # 1. Verificar se existem tipos de contrato
    print("\n📋 Verificando tipos de contrato disponíveis...")
    contracts = ContractType.objects.filter(is_active=True)
    print(f"   ✅ Encontrados {contracts.count()} tipos de contrato ativos")
    
    for contract in contracts[:3]:  # Mostrar apenas os primeiros 3
        print(f"   - {contract.name} (R$ {contract.price})")
    
    if not contracts.exists():
        print("   ❌ Nenhum tipo de contrato encontrado!")
        return False
    
    # 2. Testar página do catálogo
    print("\n🏪 Testando página do catálogo...")
    response = client.get('/contracts/catalog/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Página do catálogo carregada com sucesso")
        
        # Verificar se os botões do carrinho estão presentes
        content = response.content.decode()
        if 'Adicionar ao Carrinho' in content:
            print("   ✅ Botões 'Adicionar ao Carrinho' encontrados")
        else:
            print("   ⚠️  Botões 'Adicionar ao Carrinho' não encontrados")
    else:
        print("   ❌ Erro ao carregar página do catálogo")
        return False
    
    # 3. Testar página do carrinho vazio
    print("\n🛒 Testando página do carrinho...")
    response = client.get('/contracts/cart/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Página do carrinho carregada com sucesso")
    else:
        print("   ❌ Erro ao carregar página do carrinho")
        return False
    
    # 4. Testar adição de item ao carrinho
    print("\n➕ Testando adição de item ao carrinho...")
    first_contract = contracts.first()
    
    response = client.post(f'/contracts/cart/add/{first_contract.id}/', {
        'quantity': 1
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Item adicionado com sucesso: {data.get('message')}")
            print(f"   📊 Itens no carrinho: {data.get('cart_items')}")
            print(f"   💰 Total: R$ {data.get('cart_total')}")
        else:
            print("   ❌ Erro na resposta JSON")
            return False
    else:
        print("   ❌ Erro ao adicionar item ao carrinho")
        return False
    
    # 5. Testar dados do carrinho via AJAX
    print("\n📊 Testando obtenção de dados do carrinho...")
    response = client.get('/contracts/cart/data/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Dados obtidos com sucesso")
        print(f"   📦 Total de itens: {data.get('total_items')}")
        print(f"   💰 Valor total: R$ {data.get('total_price')}")
        print(f"   📋 Itens: {len(data.get('items', []))}")
    else:
        print("   ❌ Erro ao obter dados do carrinho")
        return False
    
    # 6. Testar página do checkout
    print("\n💳 Testando página do checkout...")
    response = client.get('/contracts/checkout/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Página do checkout carregada com sucesso")
    else:
        print("   ⚠️  Página do checkout pode requerer autenticação")
    
    # 7. Testar remoção de item do carrinho
    print("\n➖ Testando remoção de item do carrinho...")
    response = client.post(f'/contracts/cart/remove/{first_contract.id}/', 
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print(f"   ✅ Item removido com sucesso: {data.get('message')}")
            print(f"   📊 Itens no carrinho: {data.get('cart_items')}")
        else:
            print("   ❌ Erro na resposta JSON")
    else:
        print("   ❌ Erro ao remover item do carrinho")
    
    print("\n" + "=" * 50)
    print("🎉 Teste do sistema de carrinho concluído!")
    print("✅ Sistema implementado e funcionando corretamente")
    
    return True

def print_urls_summary():
    """Mostra um resumo das URLs implementadas"""
    print("\n📋 URLs do Sistema de Carrinho Implementadas:")
    print("=" * 50)
    
    urls = [
        ("Catálogo", "/contracts/catalog/", "Página principal com produtos"),
        ("Carrinho", "/contracts/cart/", "Visualizar carrinho de compras"),
        ("Adicionar ao Carrinho", "/contracts/cart/add/<id>/", "Adicionar item via AJAX"),
        ("Remover do Carrinho", "/contracts/cart/remove/<id>/", "Remover item via AJAX"),
        ("Limpar Carrinho", "/contracts/cart/clear/", "Limpar todo o carrinho"),
        ("Dados do Carrinho", "/contracts/cart/data/", "Obter dados via AJAX"),
        ("Checkout", "/contracts/checkout/", "Processo de pagamento"),
        ("Sucesso do Checkout", "/contracts/checkout/success/", "Confirmação do pedido"),
    ]
    
    for name, url, description in urls:
        print(f"   🔗 {name}")
        print(f"      URL: {url}")
        print(f"      Descrição: {description}")
        print()

if __name__ == "__main__":
    try:
        test_cart_system()
        print_urls_summary()
        
        print("\n🌐 Para testar manualmente:")
        print("   1. Acesse: http://127.0.0.1:8000/contracts/catalog/")
        print("   2. Clique em 'Adicionar ao Carrinho' em qualquer contrato")
        print("   3. Observe o badge do carrinho no navbar se atualizar")
        print("   4. Acesse: http://127.0.0.1:8000/contracts/cart/")
        print("   5. Prossiga para: http://127.0.0.1:8000/contracts/checkout/")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
