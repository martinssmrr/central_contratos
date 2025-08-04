#!/usr/bin/env python
"""
Script de teste para verificar se todas as URLs do Google OAuth estão funcionando
"""

import requests
import sys

def test_urls():
    """Testa as principais URLs da aplicação"""
    base_url = "http://127.0.0.1:8000"
    
    urls_to_test = [
        ("/", "Home page"),
        ("/users/login/", "Login page"),
        ("/users/register/", "Register page"),
        ("/accounts/google/login/", "Google OAuth login"),
        ("/admin/", "Django Admin"),
    ]
    
    print("🧪 Testando URLs da aplicação...")
    print("-" * 60)
    
    all_passed = True
    
    for url, description in urls_to_test:
        full_url = base_url + url
        try:
            response = requests.get(full_url, timeout=5)
            if response.status_code in [200, 302, 401]:  # 302 = redirect é ok
                status = "✅ OK"
                if response.status_code == 302:
                    status += f" (redirect to {response.headers.get('Location', 'unknown')})"
            else:
                status = f"❌ ERRO ({response.status_code})"
                all_passed = False
        except requests.exceptions.RequestException as e:
            status = f"❌ ERRO ({str(e)})"
            all_passed = False
        
        print(f"{description:<20} {url:<25} {status}")
    
    print("-" * 60)
    
    if all_passed:
        print("✅ Todos os testes passaram!")
        print("\n📋 Próximos passos:")
        print("1. Configure suas credenciais do Google no arquivo .env")
        print("2. Adicione as URLs de callback no Google Cloud Console")
        print("3. Teste o login com Google em: http://127.0.0.1:8000/users/login/")
    else:
        print("❌ Alguns testes falharam. Verifique se o servidor está rodando.")
    
    return all_passed

if __name__ == '__main__':
    test_urls()
