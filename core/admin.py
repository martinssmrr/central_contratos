from django.contrib import admin
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Administração das FAQs"""
    
    list_display = [
        'pergunta_resumida', 
        'ativa', 
        'ordem', 
        'criado_em',
        'atualizado_em'
    ]
    
    list_filter = [
        'ativa',
        'criado_em',
        'atualizado_em'
    ]
    
    search_fields = [
        'pergunta',
        'resposta'
    ]
    
    list_editable = [
        'ativa',
        'ordem'
    ]
    
    ordering = ['ordem', 'criado_em']
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('pergunta', 'resposta')
        }),
        ('Configurações', {
            'fields': ('ativa', 'ordem'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def get_fieldsets(self, request, obj=None):
        """Adiciona campos readonly se estiver editando"""
        fieldsets = list(self.fieldsets)
        if obj:  # Se está editando um objeto existente
            fieldsets.append(
                ('Informações do Sistema', {
                    'fields': ('criado_em', 'atualizado_em'),
                    'classes': ('collapse',)
                })
            )
        return fieldsets
    
    def save_model(self, request, obj, form, change):
        """Salva o modelo com informações extras"""
        super().save_model(request, obj, form, change)
        
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
