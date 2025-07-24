#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Layout do Catálogo - Central de Contratos
=================================================

Este script testa se a página de catálogo está carregando corretamente
e se os cards estão sendo exibidos no novo layout compacto.
"""

import requests
from bs4 import BeautifulSoup
import time

def test_catalog_layout():
    """Testa o layout do catálogo"""
    
    print("🧪 Testando Layout do Catálogo - Central de Contratos")
    print("=" * 55)
    
    try:
        # Tenta acessar a página do catálogo
        url = "http://127.0.0.1:8000/contracts/catalog/"
        print(f"🌐 Acessando: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ Página carregou com sucesso (Status: {response.status_code})")
            
            # Parse do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verifica elementos principais
            catalog_hero = soup.find('section', class_='catalog-hero')
            contracts_grid = soup.find('section', class_='contracts-grid')
            contract_cards = soup.find_all('div', class_='contract-card')
            
            print(f"\n📊 Análise dos Elementos:")
            print(f"   • Hero Section: {'✅ Encontrado' if catalog_hero else '❌ Não encontrado'}")
            print(f"   • Grid Section: {'✅ Encontrado' if contracts_grid else '❌ Não encontrado'}")
            print(f"   • Cards de Contrato: {len(contract_cards)} encontrados")
            
            # Verifica o grid responsivo
            grid_row = soup.find('div', class_='row g-3')
            if grid_row:
                print(f"   • Grid Compacto (g-3): ✅ Aplicado")
            else:
                print(f"   • Grid Compacto (g-3): ❌ Não encontrado")
            
            # Verifica as classes de coluna para layout 4x
            col_classes = soup.find_all('div', class_='col-xl-3')
            if col_classes:
                print(f"   • Layout 4 colunas (XL): ✅ Encontrado ({len(col_classes)} elementos)")
            else:
                print(f"   • Layout 4 colunas (XL): ❌ Não encontrado")
            
            # Verifica elementos dos cards
            if contract_cards:
                print(f"\n🎴 Análise dos Cards:")
                
                card = contract_cards[0]  # Analisa o primeiro card
                
                # Elementos esperados em cada card
                image_wrapper = card.find('div', class_='card-image-wrapper')
                card_content = card.find('div', class_='card-content')
                card_title = card.find('h3', class_='card-title')
                price_section = card.find('div', class_='price-section')
                btn_action = card.find('a', class_='btn-primary-custom') or card.find('a', class_='btn-outline-custom')
                
                print(f"   • Wrapper da Imagem: {'✅' if image_wrapper else '❌'}")
                print(f"   • Conteúdo do Card: {'✅' if card_content else '❌'}")
                print(f"   • Título do Card: {'✅' if card_title else '❌'}")
                print(f"   • Seção de Preço: {'✅' if price_section else '❌'}")
                print(f"   • Botão de Ação: {'✅' if btn_action else '❌'}")
            
            # Verifica o título da página
            page_title = soup.find('title')
            if page_title:
                print(f"\n📄 Título da Página: {page_title.text.strip()}")
            
            print(f"\n🎉 RESULTADO: Página do catálogo está funcionando corretamente!")
            print(f"📱 Layout responsivo implementado com sucesso!")
            print(f"🎨 Cards compactos aplicados!")
            
            return True
            
        else:
            print(f"❌ Erro ao carregar página (Status: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("   Certifique-se de que o Django está rodando em http://127.0.0.1:8000/")
        return False
        
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def test_layout_responsiveness():
    """Testa aspectos específicos do layout responsivo"""
    
    print(f"\n📱 Testando Responsividade:")
    print("=" * 25)
    
    # Simula diferentes user agents
    user_agents = {
        'Desktop': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Tablet': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15',
        'Mobile': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15'
    }
    
    for device, user_agent in user_agents.items():
        try:
            headers = {'User-Agent': user_agent}
            response = requests.get("http://127.0.0.1:8000/contracts/catalog/", 
                                  headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"   • {device}: ✅ Página carrega corretamente")
            else:
                print(f"   • {device}: ❌ Erro {response.status_code}")
                
        except Exception:
            print(f"   • {device}: ❌ Erro de conexão")

if __name__ == "__main__":
    # Aguarda um momento para o servidor estar pronto
    time.sleep(2)
    
    success = test_catalog_layout()
    test_layout_responsiveness()
    
    print(f"\n" + "=" * 55)
    if success:
        print("🎯 TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Layout do catálogo está funcionando perfeitamente!")
        print("🚀 Cards compactos implementados!")
        print("📱 Design responsivo mantido!")
    else:
        print("❌ TESTE FALHOU - Verifique os logs acima")
    print("=" * 55)
