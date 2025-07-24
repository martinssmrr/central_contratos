from django.contrib import admin
from .models import ContractType, Contract, Payment

@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

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
