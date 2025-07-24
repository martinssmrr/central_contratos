#!/usr/bin/env python
"""
Teste simples para verificar se o login está funcionando
"""

import urllib.request
import urllib.error
import sys

def simple_test():
    """Teste simples da página de login"""
    
    url = "http://127.0.0.1:8000/users/login/"
    
    try:
        print("🧪 Testando acesso à página de login...")
        
        # Fazer requisição simples
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8')
            
            print("✅ Página carregada com sucesso!")
            
            # Verificar elementos essenciais
            checks = [
                ('username', 'Campo de usuário'),
                ('password', 'Campo de senha'),
                ('Entrar', 'Botão de login'),
                ('Google', 'Botão do Google'),
                ('Esqueci', 'Link esqueci senha'),
                ('Criar', 'Link criar conta')
            ]
            
            passed = 0
            total = len(checks)
            
            print("\n📋 Verificando elementos da página:")
            for term, description in checks:
                if term.lower() in content.lower():
                    print(f"   ✅ {description}")
                    passed += 1
                else:
                    print(f"   ❌ {description}")
            
            print(f"\n📊 Resultado: {passed}/{total} elementos encontrados")
            
            if passed >= 5:  # Pelo menos 5 dos 6 elementos
                print("🎉 SUCESSO! Página de login está funcionando!")
                return True
            else:
                print("⚠️  Alguns elementos não foram encontrados.")
                return False
                
    except urllib.error.URLError as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == '__main__':
    print("🎯 TESTE SIMPLES DA PÁGINA DE LOGIN")
    print("=" * 50)
    
    success = simple_test()
    
    if success:
        print("\n✅ Teste concluído com sucesso!")
        print("🔗 Acesse: http://127.0.0.1:8000/users/login/")
    else:
        print("\n❌ Teste falhou.")
    
    sys.exit(0 if success else 1)
