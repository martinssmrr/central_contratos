from django.db import migrations, models
import django.db.models.deletion


def create_categories_from_existing_data(apps, schema_editor):
    """Criar categorias baseadas nos dados existentes"""
    ContractType = apps.get_model('contracts', 'ContractType')
    Category = apps.get_model('contracts', 'Category')
    
    # Obter todas as categorias únicas existentes
    existing_categories = set()
    for contract_type in ContractType.objects.all():
        if contract_type.category:
            existing_categories.add(contract_type.category)
    
    # Criar categorias padrão se não existirem dados
    if not existing_categories:
        default_categories = [
            ('Locação', 'locacao', 'Contratos de locação residencial e comercial', 'fas fa-home', '#4CAF50'),
            ('Compra e Venda', 'compra-venda', 'Contratos de compra e venda de imóveis', 'fas fa-exchange-alt', '#2196F3'),
            ('Prestação de Serviços', 'prestacao-servicos', 'Contratos de prestação de serviços', 'fas fa-handshake', '#FF9800'),
            ('Freelancer', 'freelancer', 'Contratos para trabalho freelancer', 'fas fa-laptop-code', '#9C27B0'),
            ('Confissão de Dívidas', 'confissao-dividas', 'Contratos de confissão de dívidas', 'fas fa-file-invoice-dollar', '#F44336'),
        ]
        
        for name, slug, desc, icon, color in default_categories:
            Category.objects.create(
                name=name,
                slug=slug,
                description=desc,
                icon=icon,
                color=color,
                is_active=True
            )
    else:
        # Criar categorias baseadas nos dados existentes
        category_mapping = {
            'Locação': ('locacao', 'Contratos de locação', 'fas fa-home', '#4CAF50'),
            'Compra e Venda': ('compra-venda', 'Contratos de compra e venda', 'fas fa-exchange-alt', '#2196F3'),
            'Prestação de Serviços': ('prestacao-servicos', 'Contratos de serviços', 'fas fa-handshake', '#FF9800'),
            'Freelancer': ('freelancer', 'Contratos freelancer', 'fas fa-laptop-code', '#9C27B0'),
            'Confissão de Dívidas': ('confissao-dividas', 'Confissão de dívidas', 'fas fa-file-invoice-dollar', '#F44336'),
        }
        
        for category_name in existing_categories:
            if category_name in category_mapping:
                slug, desc, icon, color = category_mapping[category_name]
            else:
                from django.utils.text import slugify
                slug = slugify(category_name)
                desc = f'Contratos de {category_name.lower()}'
                icon = 'fas fa-file-contract'
                color = '#f4623a'
            
            Category.objects.create(
                name=category_name,
                slug=slug,
                description=desc,
                icon=icon,
                color=color,
                is_active=True
            )


def migrate_contract_types_to_categories(apps, schema_editor):
    """Migrar os tipos de contrato para usar as novas categorias"""
    ContractType = apps.get_model('contracts', 'ContractType')
    Category = apps.get_model('contracts', 'Category')
    
    for contract_type in ContractType.objects.all():
        if contract_type.category:
            try:
                category = Category.objects.get(name=contract_type.category)
                contract_type.category_new = category
                contract_type.save()
            except Category.DoesNotExist:
                # Se a categoria não existir, deixar nulo
                pass


def reverse_migration(apps, schema_editor):
    """Reverter a migração"""
    ContractType = apps.get_model('contracts', 'ContractType')
    
    for contract_type in ContractType.objects.all():
        if hasattr(contract_type, 'category_new') and contract_type.category_new:
            contract_type.category = contract_type.category_new.name
            contract_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0007_auto_20250728_1348'),
    ]

    operations = [
        # 1. Criar o modelo Category
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('icon', models.CharField(default='fas fa-folder', help_text='Ex: fas fa-building, fas fa-handshake', max_length=50, verbose_name='Ícone FontAwesome')),
                ('color', models.CharField(default='#f4623a', help_text='Cor em hexadecimal (ex: #f4623a)', max_length=7, verbose_name='Cor')),
                ('order', models.PositiveIntegerField(default=0, help_text='Menor número aparece primeiro', verbose_name='Ordem de Exibição')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['order', 'name'],
            },
        ),
        
        # 2. Criar categorias baseadas nos dados existentes
        migrations.RunPython(create_categories_from_existing_data, reverse_migration),
        
        # 3. Adicionar novo campo ForeignKey temporário
        migrations.AddField(
            model_name='contracttype',
            name='category_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_types_temp', to='contracts.category', verbose_name='Nova Categoria'),
        ),
        
        # 4. Migrar dados para o novo campo
        migrations.RunPython(migrate_contract_types_to_categories, reverse_migration),
        
        # 5. Remover o campo antigo
        migrations.RemoveField(
            model_name='contracttype',
            name='category',
        ),
        
        # 6. Renomear o novo campo
        migrations.RenameField(
            model_name='contracttype',
            old_name='category_new',
            new_name='category',
        ),
        
        # 7. Atualizar o campo para o estado final
        migrations.AlterField(
            model_name='contracttype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_types', to='contracts.category', verbose_name='Categoria'),
        ),
    ]
