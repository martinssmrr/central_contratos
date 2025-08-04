#!/usr/bin/env python3
"""
Teste das páginas de login e registro
"""

import requests
from bs4 import BeautifulSoup

def test_login_page():
    """Testa a página de login"""
    try:
        response = requests.get('http://127.0.0.1:8000/users/login/')
        print(f"📍 Status da página de login: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar elementos essenciais
            elements_to_check = [
                ('input[name="username"]', 'Campo de usuário'),
                ('input[name="password"]', 'Campo de senha'),
                ('button[type="submit"]', 'Botão de login'),
                ('.btn-google', 'Botão do Google'),
                ('a[href*="register"]', 'Link para registro'),
                ('a[href*="password"]', 'Link esqueci senha')
            ]
            
            found_elements = 0
            total_elements = len(elements_to_check)
            
            for selector, description in elements_to_check:
                element = soup.select_one(selector)
                if element:
                    print(f"✅ {description}: encontrado")
                    found_elements += 1
                else:
                    print(f"❌ {description}: não encontrado")
            
            print(f"\n📊 Elementos encontrados: {found_elements}/{total_elements}")
            return found_elements == total_elements
        else:
            print(f"❌ Erro ao acessar página de login: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar página de login: {e}")
        return False

def test_register_page():
    """Testa a página de registro"""
    try:
        response = requests.get('http://127.0.0.1:8000/users/register/')
        print(f"\n📍 Status da página de registro: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar elementos essenciais
            elements_to_check = [
                ('input[name="first_name"]', 'Campo de nome'),
                ('input[name="last_name"]', 'Campo de sobrenome'),
                ('input[name="username"]', 'Campo de usuário'),
                ('input[name="email"]', 'Campo de email'),
                ('input[name="password1"]', 'Campo de senha'),
                ('input[name="password2"]', 'Campo confirmar senha'),
                ('button[type="submit"]', 'Botão de registro'),
                ('.btn-google', 'Botão do Google'),
                ('a[href*="login"]', 'Link para login')
            ]
            
            found_elements = 0
            total_elements = len(elements_to_check)
            
            for selector, description in elements_to_check:
                element = soup.select_one(selector)
                if element:
                    print(f"✅ {description}: encontrado")
                    found_elements += 1
                else:
                    print(f"❌ {description}: não encontrado")
            
            print(f"\n📊 Elementos encontrados: {found_elements}/{total_elements}")
            return found_elements == total_elements
        else:
            print(f"❌ Erro ao acessar página de registro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar página de registro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando páginas de usuário...")
    print("=" * 50)
    
    login_ok = test_login_page()
    register_ok = test_register_page()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES:")
    print(f"   🔐 Página de Login: {'✅ OK' if login_ok else '❌ ERRO'}")
    print(f"   📝 Página de Registro: {'✅ OK' if register_ok else '❌ ERRO'}")
    
    if login_ok and register_ok:
        print("\n🎉 SUCESSO! Todas as páginas estão funcionando! ✅")
    else:
        print("\n⚠️  Algumas páginas precisam de ajustes ❌")
