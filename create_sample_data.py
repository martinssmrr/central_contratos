#!/usr/bin/env python
"""
Script simplificado para recriar dados essenciais no MySQL
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from contracts.models import ContractType, Category
from core.models import FAQ

def create_sample_data():
    """Cria dados de exemplo para o sistema"""
    
    print("🔧 Criando dados essenciais...")
    
    # 1. Criar categorias
    categories_data = [
        ('IMOBILIÁRIO', 'imobiliario', 'Contratos relacionados a imóveis'),
        ('COMERCIAL', 'comercial', 'Contratos comerciais e empresariais'),
        ('TRABALHO', 'trabalho', 'Contratos de trabalho e prestação de serviços'),
        ('FINANCEIRO', 'financeiro', 'Contratos financeiros e empréstimos'),
        ('AUTOMOTIVO', 'automotivo', 'Contratos relacionados a veículos'),
    ]
    
    for name, slug, description in categories_data:
        category, created = Category.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
                'is_active': True
            }
        )
        if created:
            print(f"  ✅ Categoria criada: {category.name}")
    
    # 2. Criar tipos de contrato
    contracts_data = [
        ('Contrato de Compra e Venda de Imóvel', 'compra-venda-imovel', 
         'Contrato para compra e venda de imóveis residenciais e comerciais', 
         'imobiliario', Decimal('59.90'), '#e74c3c'),
        
        ('Contrato de Locação Residencial', 'locacao-residencial',
         'Contrato para locação de imóveis residenciais',
         'imobiliario', Decimal('39.90'), '#3498db'),
        
        ('Contrato de Prestação de Serviços', 'prestacao-servicos',
         'Contrato para prestação de serviços profissionais',
         'comercial', Decimal('49.90'), '#2ecc71'),
        
        ('Contrato Free Lancer', 'freelancer',
         'Contrato para trabalhos freelancer e autônomos',
         'trabalho', Decimal('29.90'), '#f39c12'),
        
        ('Contrato de Locação Comercial', 'locacao-comercial',
         'Contrato para locação de imóveis comerciais',
         'imobiliario', Decimal('69.90'), '#9b59b6'),
        
        ('Contrato de Confissão de Dívidas', 'confissao-dividas',
         'Contrato para confissão e parcelamento de dívidas',
         'financeiro', Decimal('39.90'), '#e67e22'),
        
        ('Contrato de Compra e Venda de Automóvel', 'compra-venda-automovel',
         'Contrato para compra e venda de veículos automotores',
         'automotivo', Decimal('34.90'), '#1abc9c'),
    ]
    
    for name, slug, description, cat_slug, price, color in contracts_data:
        try:
            category = Category.objects.get(slug=cat_slug)
            contract, created = ContractType.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': description,
                    'category': category,
                    'price': price,
                    'color': color,
                    'is_active': True,
                    'order': 0
                }
            )
            if created:
                print(f"  ✅ Contrato criado: {contract.name}")
        except Exception as e:
            print(f"  ⚠️ Erro ao criar contrato {name}: {e}")
    
    # 3. Criar FAQs
    faqs_data = [
        ('Como funciona o download do contrato?', 
         'Após a compra, você receberá um link para download do contrato em formato Word (.docx), pronto para edição e preenchimento.'),
        
        ('Os contratos são válidos juridicamente?', 
         'Sim! Todos os nossos contratos são elaborados por advogados especializados e seguem a legislação brasileira vigente.'),
        
        ('Posso editar o contrato após o download?', 
         'Sim, o arquivo vem em formato editável para que você possa personalizar conforme suas necessidades específicas.'),
        
        ('Qual a forma de pagamento?', 
         'Aceitamos pagamentos via Mercado Pago (cartão de crédito, débito, PIX e boleto bancário).'),
        
        ('Oferecem suporte jurídico?', 
         'Nossos contratos são modelos padrão. Para casos específicos, recomendamos consultar um advogado.'),
        
        ('Posso usar o contrato quantas vezes quiser?', 
         'Sim, após a compra, você pode usar o modelo quantas vezes precisar.'),
        
        ('Como faço para entrar em contato?', 
         'Você pode nos contatar através do email contato@centraldecontratos.com ou pelo formulário de contato.'),
        
        ('Há garantia de satisfação?', 
         'Sim, oferecemos garantia de 30 dias. Se não ficar satisfeito, devolvemos seu dinheiro.')
    ]
    
    for i, (pergunta, resposta) in enumerate(faqs_data):
        faq, created = FAQ.objects.get_or_create(
            pergunta=pergunta,
            defaults={
                'resposta': resposta,
                'ativa': True,
                'ordem': i + 1
            }
        )
        if created:
            print(f"  ✅ FAQ criada: {faq.pergunta[:50]}...")
    
    # 4. Criar usuário demo (além do admin)
    if not User.objects.filter(username='demo').exists():
        demo_user = User.objects.create_user(
            username='demo',
            email='demo@centralcontratos.com',
            password='demo123',
            first_name='Demo',
            last_name='User',
            is_active=True
        )
        print(f"  ✅ Usuário demo criado: {demo_user.username}")
    
    # Relatório final
    print("\n📊 DADOS CRIADOS COM SUCESSO:")
    print(f"✅ Categorias: {Category.objects.count()}")
    print(f"✅ Tipos de Contrato: {ContractType.objects.count()}")
    print(f"✅ FAQs: {FAQ.objects.count()}")
    print(f"✅ Usuários: {User.objects.count()}")
    print("\n🎉 Sistema pronto para uso!")

if __name__ == "__main__":
    create_sample_data()
