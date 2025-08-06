#!/usr/bin/env python
"""
Script para extrair dados do SQLite e recriar no MySQL
"""
import os
import sys
import django
import sqlite3
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from contracts.models import ContractType, Category
from core.models import FAQ
from users.models import UserProfile

def extract_and_recreate_data():
    """Extrai dados do SQLite e recria no MySQL"""
    
    # Conectar ao SQLite
    sqlite_path = 'db.sqlite3'
    if not os.path.exists(sqlite_path):
        print("❌ Arquivo SQLite não encontrado!")
        return
    
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    
    print("🔍 Extraindo dados do SQLite...")
    
    # 1. Extrair e recriar categorias
    try:
        cursor.execute("SELECT * FROM contracts_category")
        categories = cursor.fetchall()
        
        print(f"📁 Encontradas {len(categories)} categorias")
        
        for cat in categories:
            category, created = Category.objects.get_or_create(
                id=cat[0],
                defaults={
                    'name': cat[1],
                    'slug': cat[2],
                    'description': cat[3] or '',
                    'is_active': bool(cat[4])
                }
            )
            if created:
                print(f"  ✅ Categoria criada: {category.name}")
    except Exception as e:
        print(f"  ⚠️ Erro ao extrair categorias: {e}")
    
    # 2. Extrair e recriar tipos de contrato
    try:
        cursor.execute("SELECT * FROM contracts_contracttype")
        contracts = cursor.fetchall()
        
        print(f"📄 Encontrados {len(contracts)} tipos de contrato")
        
        for contract in contracts:
            try:
                # Buscar categoria se existir
                category = None
                if contract[4]:  # category_id
                    try:
                        category = Category.objects.get(id=contract[4])
                    except Category.DoesNotExist:
                        pass
                
                contract_type, created = ContractType.objects.get_or_create(
                    id=contract[0],
                    defaults={
                        'name': contract[1],
                        'slug': contract[2],
                        'description': contract[3] or '',
                        'category': category,
                        'price': Decimal(str(contract[5])) if contract[5] else Decimal('0.00'),
                        'is_active': bool(contract[6]),
                        'order': contract[7] or 0,
                        'color': contract[10] or '#f4623a'
                    }
                )
                if created:
                    print(f"  ✅ Contrato criado: {contract_type.name}")
            except Exception as e:
                print(f"  ⚠️ Erro ao criar contrato {contract[1]}: {e}")
    except Exception as e:
        print(f"  ⚠️ Erro ao extrair contratos: {e}")
    
    # 3. Extrair e recriar FAQs
    try:
        cursor.execute("SELECT * FROM core_faq")
        faqs = cursor.fetchall()
        
        print(f"❓ Encontradas {len(faqs)} FAQs")
        
        for faq in faqs:
            faq_obj, created = FAQ.objects.get_or_create(
                id=faq[0],
                defaults={
                    'pergunta': faq[1],
                    'resposta': faq[2],
                    'ativa': bool(faq[3]),
                    'ordem': faq[4] or 0
                }
            )
            if created:
                print(f"  ✅ FAQ criada: {faq_obj.question[:50]}...")
    except Exception as e:
        print(f"  ⚠️ Erro ao extrair FAQs: {e}")
    
    # 4. Extrair e recriar usuários
    try:
        cursor.execute("SELECT * FROM auth_user")
        users = cursor.fetchall()
        
        print(f"👤 Encontrados {len(users)} usuários")
        
        for user_data in users:
            try:
                # Pular usuários que já existem (como admin)
                if User.objects.filter(username=user_data[4]).exists():
                    print(f"  ⚠️ Usuário {user_data[4]} já existe")
                    continue
                    
                user = User.objects.create(
                    username=user_data[4],
                    password=user_data[1],
                    last_login=user_data[2],
                    is_superuser=bool(user_data[3]),
                    first_name=user_data[5] or '',
                    last_name=user_data[6] or '',
                    email=user_data[7] or '',
                    is_staff=bool(user_data[8]),
                    is_active=bool(user_data[9]),
                    date_joined=user_data[10]
                )
                print(f"  ✅ Usuário criado: {user.username}")
            except Exception as e:
                print(f"  ⚠️ Erro ao criar usuário {user_data[4]}: {e}")
    except Exception as e:
        print(f"  ⚠️ Erro ao extrair usuários: {e}")
    
    # 5. Extrair perfis de usuários
    try:
        cursor.execute("SELECT * FROM users_userprofile")
        profiles = cursor.fetchall()
        
        print(f"👤 Encontrados {len(profiles)} perfis de usuário")
        
        for profile_data in profiles:
            try:
                if not profile_data[1]:  # Se user_id está vazio
                    continue
                    
                user = User.objects.get(id=profile_data[1])
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'bio': profile_data[2] or '',
                        'phone': profile_data[3] or '',
                        'birth_date': profile_data[4],
                        'is_verified': bool(profile_data[5]) if profile_data[5] else False,
                        'user_type': profile_data[8] or 'cliente'
                    }
                )
                if created:
                    print(f"  ✅ Perfil criado para: {user.username}")
            except Exception as e:
                print(f"  ⚠️ Erro ao criar perfil: {e}")
    except Exception as e:
        print(f"  ⚠️ Erro ao extrair perfis: {e}")
    
    conn.close()
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL:")
    print(f"✅ Categorias: {Category.objects.count()}")
    print(f"✅ Tipos de Contrato: {ContractType.objects.count()}")
    print(f"✅ FAQs: {FAQ.objects.count()}")
    print(f"✅ Usuários: {User.objects.count()}")
    print(f"✅ Perfis: {UserProfile.objects.count()}")
    print("\n🎉 Migração concluída!")

if __name__ == "__main__":
    extract_and_recreate_data()
