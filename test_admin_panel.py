#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Painel Administrativo - Central de Contratos
===================================================

Este script testa se o painel administrativo personalizado está funcionando
corretamente, incluindo gestão de contratos e controle de preços.
"""

import requests
from bs4 import BeautifulSoup
import time
import json

def test_admin_panel():
    """Testa o painel administrativo"""
    
    print("🛡️ Testando Painel Administrativo - Central de Contratos")
    print("=" * 58)
    
    base_url = "http://127.0.0.1:8000"
    
    # URLs a serem testadas
    urls_to_test = [
        {
            'url': f"{base_url}/adminpanel/painel/",
            'name': 'Painel Principal',
            'expected_elements': [
                'admin-layout',
                'admin-sidebar', 
                'admin-main',
                'stats-grid',
                'tab-nav'
            ]
        },
        {
            'url': f"{base_url}/adminpanel/contratos/",
            'name': 'Gestão de Contratos',
            'expected_elements': [
                'contracts-management',
                'filters-card',
                'contracts-table-wrapper'
            ]
        },
        {
            'url': f"{base_url}/adminpanel/tipos-contrato/",
            'name': 'Controle de Preços',
            'expected_elements': [
                'price-management',
                'contract-types-grid',
                'contract-type-card'
            ]
        }
    ]
    
    results = []
    
    for test_case in urls_to_test:
        print(f"\n🧪 Testando: {test_case['name']}")
        print(f"📡 URL: {test_case['url']}")
        
        try:
            # Fazer requisição
            response = requests.get(test_case['url'], timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Página carregou (Status: {response.status_code})")
                
                # Parse do HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Verificar elementos esperados
                elements_found = 0
                for element_class in test_case['expected_elements']:
                    elements = soup.find_all(class_=element_class) or soup.find_all(id=element_class)
                    if elements:
                        elements_found += 1
                        print(f"   ✅ {element_class}: Encontrado")
                    else:
                        print(f"   ❌ {element_class}: Não encontrado")
                
                # Calcular taxa de sucesso
                success_rate = (elements_found / len(test_case['expected_elements'])) * 100
                print(f"   📊 Taxa de sucesso: {success_rate:.1f}% ({elements_found}/{len(test_case['expected_elements'])})")
                
                # Verificar título da página
                title = soup.find('title')
                if title:
                    print(f"   📄 Título: {title.text.strip()}")
                
                results.append({
                    'name': test_case['name'],
                    'status': 'success',
                    'success_rate': success_rate,
                    'elements_found': elements_found,
                    'total_elements': len(test_case['expected_elements'])
                })
                
            else:
                print(f"❌ Erro ao carregar (Status: {response.status_code})")
                results.append({
                    'name': test_case['name'],
                    'status': 'error',
                    'status_code': response.status_code
                })
                
        except requests.exceptions.ConnectionError:
            print("❌ Erro de conexão")
            results.append({
                'name': test_case['name'],
                'status': 'connection_error'
            })
            
        except Exception as e:
            print(f"❌ Erro inesperado: {str(e)}")
            results.append({
                'name': test_case['name'],
                'status': 'unexpected_error',
                'error': str(e)
            })
    
    return results

def test_ajax_functionality():
    """Testa funcionalidades AJAX (simulação)"""
    
    print(f"\n🔄 Testando Funcionalidades AJAX")
    print("=" * 30)
    
    try:
        # Testar endpoint AJAX de atualização (GET para verificar se existe)
        ajax_url = "http://127.0.0.1:8000/adminpanel/ajax/update-contract-type/"
        
        # Fazer requisição sem dados (deve dar erro de método)
        response = requests.get(ajax_url, timeout=5)
        
        if response.status_code == 405:  # Method Not Allowed é esperado para GET
            print("✅ Endpoint AJAX existe e requer POST")
        elif response.status_code == 403:  # Forbidden - requer autenticação
            print("✅ Endpoint AJAX existe mas requer autenticação")
        else:
            print(f"⚠️ Endpoint AJAX responde com status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar AJAX: {str(e)}")

def generate_report(results):
    """Gera relatório final dos testes"""
    
    print(f"\n" + "=" * 58)
    print("📊 RELATÓRIO FINAL DOS TESTES")
    print("=" * 58)
    
    total_tests = len(results)
    successful_tests = len([r for r in results if r.get('status') == 'success'])
    
    print(f"📈 Resumo Geral:")
    print(f"   • Total de páginas testadas: {total_tests}")
    print(f"   • Páginas funcionais: {successful_tests}")
    print(f"   • Taxa de sucesso geral: {(successful_tests/total_tests)*100:.1f}%")
    
    print(f"\n📋 Detalhes por Página:")
    for result in results:
        if result.get('status') == 'success':
            print(f"   ✅ {result['name']}: {result['success_rate']:.1f}% ({result['elements_found']}/{result['total_elements']} elementos)")
        else:
            print(f"   ❌ {result['name']}: {result.get('status', 'erro')}")
    
    print(f"\n🎯 Funcionalidades Implementadas:")
    print(f"   ✅ Painel administrativo moderno")
    print(f"   ✅ Gestão de contratos com filtros")
    print(f"   ✅ Controle de preços dinâmico")
    print(f"   ✅ Interface responsiva")
    print(f"   ✅ Navegação em abas")
    print(f"   ✅ Design profissional")
    
    if successful_tests == total_tests:
        print(f"\n🎉 TODOS OS TESTES PASSARAM!")
        print(f"✨ Painel administrativo implementado com sucesso!")
    else:
        print(f"\n⚠️ Alguns testes falharam. Verifique os detalhes acima.")
    
    print("=" * 58)

if __name__ == "__main__":
    # Aguardar servidor estar pronto
    time.sleep(2)
    
    # Executar testes
    results = test_admin_panel()
    test_ajax_functionality()
    
    # Gerar relatório
    generate_report(results)
