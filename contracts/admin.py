from django.contrib import admin
from .models import Category, ContractType, Contract, Payment, CompraVendaImovel, ContratoCompraVendaImovel, ContratoLocacaoResidencial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'order', 'is_active', 'get_contracts_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'get_contracts_count']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Aparência', {
            'fields': ('icon', 'color', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Estatísticas', {
            'fields': ('get_contracts_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_contracts_count(self, obj):
        return obj.get_contracts_count()
    get_contracts_count.short_description = 'Tipos de Contrato'

@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    list_editable = ['is_active']

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'contract_type', 'status', 'valor', 'created_at']
    list_filter = ['status', 'contract_type', 'created_at']
    search_fields = ['parte1_nome', 'parte2_nome', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'contract_type', 'status', 'pdf_file')
        }),
        ('Primeira Parte', {
            'fields': ('parte1_nome', 'parte1_cpf_cnpj', 'parte1_endereco')
        }),
        ('Segunda Parte', {
            'fields': ('parte2_nome', 'parte2_cpf_cnpj', 'parte2_endereco')
        }),
        ('Dados do Contrato', {
            'fields': ('objeto_contrato', 'valor', 'forma_pagamento', 'data_inicio', 'data_fim', 'prazo_vigencia')
        }),
        ('Dados Específicos', {
            'fields': ('dados_especificos',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['contract', 'status', 'payment_method', 'amount', 'payment_date', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['contract__parte1_nome', 'contract__parte2_nome', 'transaction_id']
    readonly_fields = ['created_at']
    date_hierarchy = 'payment_date'


@admin.register(CompraVendaImovel)
class CompraVendaImovelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'imovel_tipo', 'valor_total', 'forma_pagamento', 'status', 'created_at']
    list_filter = ['status', 'imovel_tipo', 'forma_pagamento', 'created_at']
    search_fields = ['proprietario_nome', 'comprador_nome', 'imovel_rua', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'status')
        }),
        ('Proprietário', {
            'fields': (
                'proprietario_nome', 'proprietario_estado_civil', 'proprietario_nacionalidade', 
                'proprietario_profissao', 'proprietario_rg', 'proprietario_cpf'
            )
        }),
        ('Endereço do Proprietário', {
            'fields': (
                'proprietario_rua', 'proprietario_numero', 'proprietario_bairro', 
                'proprietario_cidade', 'proprietario_estado', 'proprietario_cep'
            )
        }),
        ('Cônjuge do Proprietário', {
            'fields': (
                'proprietario_conjuge_nome', 'proprietario_conjuge_nacionalidade', 
                'proprietario_conjuge_profissao', 'proprietario_conjuge_rg', 'proprietario_conjuge_cpf'
            ),
            'classes': ('collapse',)
        }),
        ('Comprador', {
            'fields': (
                'comprador_nome', 'comprador_estado_civil', 'comprador_nacionalidade', 
                'comprador_profissao', 'comprador_rg', 'comprador_cpf'
            )
        }),
        ('Endereço do Comprador', {
            'fields': (
                'comprador_rua', 'comprador_numero', 'comprador_bairro', 
                'comprador_cidade', 'comprador_estado', 'comprador_cep'
            )
        }),
        ('Cônjuge do Comprador', {
            'fields': (
                'comprador_conjuge_nome', 'comprador_conjuge_nacionalidade', 
                'comprador_conjuge_profissao', 'comprador_conjuge_rg', 'comprador_conjuge_cpf'
            ),
            'classes': ('collapse',)
        }),
        ('Imóvel', {
            'fields': (
                'imovel_tipo', 'imovel_rua', 'imovel_numero', 'imovel_bairro', 
                'imovel_cidade', 'imovel_estado', 'imovel_cep'
            )
        }),
        ('Dados Registrais do Imóvel', {
            'fields': (
                'imovel_matricula', 'imovel_cartorio', 'imovel_iptu', 
                'imovel_area_territorial', 'imovel_area_construida'
            )
        }),
        ('Detalhes da Venda', {
            'fields': (
                'valor_total', 'valor_extenso', 'forma_pagamento', 'data_pagamento', 
                'conta_bancaria', 'data_entrega'
            )
        }),
        ('Parcelamento', {
            'fields': ('quantidade_parcelas', 'datas_parcelas'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.status == 'assinado':
            # Se o contrato já foi assinado, tornar a maioria dos campos apenas leitura
            readonly.extend([
                'proprietario_nome', 'comprador_nome', 'valor_total', 'imovel_rua'
            ])
        return readonly


@admin.register(ContratoCompraVendaImovel)
class ContratoCompraVendaImovelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'valor_total', 'forma_pagamento', 'created_at']
    list_filter = ['status', 'forma_pagamento', 'proprietario_estado_civil', 'comprador_estado_civil', 'imovel_tipo', 'created_at']
    search_fields = ['proprietario_nome', 'comprador_nome', 'user__username', 'imovel_endereco_rua']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'status')
        }),
        ('Proprietário', {
            'fields': (
                'proprietario_nome', 'proprietario_estado_civil', 'proprietario_nacionalidade',
                'proprietario_profissao', 'proprietario_rg', 'proprietario_cpf',
                'proprietario_endereco_rua', 'proprietario_endereco_numero', 'proprietario_endereco_bairro',
                'proprietario_endereco_cidade', 'proprietario_endereco_estado', 'proprietario_endereco_cep'
            )
        }),
        ('Cônjuge do Proprietário', {
            'fields': (
                'proprietario_conjuge_nome', 'proprietario_conjuge_nacionalidade',
                'proprietario_conjuge_profissao', 'proprietario_conjuge_rg', 'proprietario_conjuge_cpf'
            ),
            'classes': ('collapse',)
        }),
        ('Comprador', {
            'fields': (
                'comprador_nome', 'comprador_estado_civil', 'comprador_nacionalidade',
                'comprador_profissao', 'comprador_rg', 'comprador_cpf',
                'comprador_endereco_rua', 'comprador_endereco_numero', 'comprador_endereco_bairro',
                'comprador_endereco_cidade', 'comprador_endereco_estado', 'comprador_endereco_cep'
            )
        }),
        ('Cônjuge do Comprador', {
            'fields': (
                'comprador_conjuge_nome', 'comprador_conjuge_nacionalidade',
                'comprador_conjuge_profissao', 'comprador_conjuge_rg', 'comprador_conjuge_cpf'
            ),
            'classes': ('collapse',)
        }),
        ('Imóvel', {
            'fields': (
                'imovel_tipo', 'imovel_matricula', 'imovel_cartorio', 'imovel_iptu',
                'imovel_endereco_rua', 'imovel_endereco_numero', 'imovel_endereco_bairro',
                'imovel_endereco_cidade', 'imovel_endereco_estado', 'imovel_endereco_cep',
                'imovel_area_territorial', 'imovel_area_construida'
            )
        }),
        ('Detalhes da Venda', {
            'fields': (
                'valor_total', 'valor_extenso', 'forma_pagamento', 'data_pagamento',
                'data_entrega', 'conta_bancaria'
            )
        }),
        ('Parcelamento', {
            'fields': ('quantidade_parcelas', 'datas_parcelas'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj and obj.status == 'assinado':
            # Se o contrato já foi assinado, tornar a maioria dos campos apenas leitura
            readonly.extend([
                'proprietario_nome', 'comprador_nome', 'valor_total', 
                'imovel_endereco_rua', 'forma_pagamento'
            ])
        return readonly


@admin.register(ContratoLocacaoResidencial)
class ContratoLocacaoResidencialAdmin(admin.ModelAdmin):
    """Admin para contratos de locação residencial"""
    
    list_display = [
        'proprietario_nome', 'locatario_nome', 'imovel_tipo', 
        'valor_aluguel', 'data_inicio', 'data_termino', 'created_at'
    ]
    
    list_filter = [
        'imovel_tipo', 'forma_pagamento', 'tipo_garantia', 
        'data_inicio', 'data_termino', 'created_at'
    ]
    
    search_fields = [
        'proprietario_nome', 'locatario_nome', 'proprietario_cpf', 
        'locatario_cpf', 'imovel_rua', 'imovel_cidade'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('Proprietário', {
            'fields': (
                'proprietario_nome', 'proprietario_estado_civil', 'proprietario_nacionalidade',
                'proprietario_profissao', 'proprietario_rg', 'proprietario_cpf',
                'proprietario_rua', 'proprietario_numero', 'proprietario_bairro',
                'proprietario_cidade', 'proprietario_estado'
            )
        }),
        ('Cônjuge do Proprietário', {
            'fields': (
                'proprietario_conjuge_nome', 'proprietario_conjuge_nacionalidade',
                'proprietario_conjuge_profissao', 'proprietario_conjuge_rg', 
                'proprietario_conjuge_cpf'
            ),
            'classes': ('collapse',)
        }),
        ('Locatário', {
            'fields': (
                'locatario_nome', 'locatario_estado_civil', 'locatario_nacionalidade',
                'locatario_profissao', 'locatario_rg', 'locatario_cpf',
                'locatario_rua', 'locatario_numero', 'locatario_bairro',
                'locatario_cidade', 'locatario_estado'
            )
        }),
        ('Cônjuge do Locatário', {
            'fields': (
                'locatario_conjuge_nome', 'locatario_conjuge_nacionalidade',
                'locatario_conjuge_profissao', 'locatario_conjuge_rg', 
                'locatario_conjuge_cpf'
            ),
            'classes': ('collapse',)
        }),
        ('Imóvel', {
            'fields': (
                'imovel_tipo', 'imovel_rua', 'imovel_numero', 'imovel_bairro',
                'imovel_cidade', 'imovel_estado', 'imovel_matricula', 
                'imovel_cartorio', 'imovel_iptu', 'imovel_conta_agua', 'imovel_conta_luz'
            )
        }),
        ('Detalhes da Locação', {
            'fields': (
                'valor_aluguel', 'valor_aluguel_extenso', 'forma_pagamento',
                'dia_pagamento', 'conta_bancaria', 'data_inicio', 'data_termino'
            )
        }),
        ('Garantia', {
            'fields': (
                'tipo_garantia', 'valor_caucao'
            )
        }),
        ('Fiador/Avalista', {
            'fields': (
                'fiador_nome', 'fiador_estado_civil', 'fiador_nacionalidade',
                'fiador_profissao', 'fiador_rg', 'fiador_cpf',
                'fiador_rua', 'fiador_numero', 'fiador_bairro',
                'fiador_cidade', 'fiador_estado'
            ),
            'classes': ('collapse',)
        }),
        ('Seguro Fiança', {
            'fields': (
                'seguro_nome_seguradora', 'seguro_prazo', 'seguro_valor'
            ),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and not request.user.is_superuser:
            # Para usuários não superusuários, tornar alguns campos apenas leitura
            readonly.extend([
                'proprietario_nome', 'locatario_nome', 'valor_aluguel', 
                'imovel_rua', 'forma_pagamento'
            ])
        return readonly
