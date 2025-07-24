from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class ContractType(models.Model):
    """Tipos de contratos disponíveis"""
    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    image = models.ImageField('Imagem', upload_to='contract_types/', blank=True, null=True)
    category = models.CharField('Categoria', max_length=50, blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    icon = models.CharField('Ícone FontAwesome', max_length=50, default='fas fa-file-contract', 
                           help_text='Ex: fas fa-file-contract, fas fa-building')
    color = models.CharField('Cor', max_length=7, default='#f4623a', 
                           help_text='Cor em hexadecimal (ex: #f4623a)')
    order = models.PositiveIntegerField('Ordem de Exibição', default=0, 
                                      help_text='Menor número aparece primeiro')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Tipo de Contrato'
        verbose_name_plural = 'Tipos de Contratos'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('contracts:contract_form', kwargs={'slug': self.slug})
    
    def get_contracts_count(self):
        """Retorna o número de contratos vinculados a este tipo"""
        return self.contract_set.count()
    
    def get_active_contracts_count(self):
        """Retorna o número de contratos ativos vinculados a este tipo"""
        return self.contract_set.filter(status='paid').count()
    
    def save(self, *args, **kwargs):
        """Auto-gerar slug se não fornecido"""
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
            # Garantir unicidade do slug
            original_slug = self.slug
            counter = 1
            while ContractType.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class Contract(models.Model):
    """Contratos gerados pelos usuários"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('cancelled', 'Cancelado'),
    ]
    
    # Relacionamentos
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE, verbose_name='Tipo de Contrato')
    
    # Dados básicos
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    pdf_file = models.FileField('Arquivo PDF', upload_to='contracts/', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    # Dados das partes (comum a todos os contratos)
    parte1_nome = models.CharField('Nome da Parte 1', max_length=200)
    parte1_cpf_cnpj = models.CharField('CPF/CNPJ da Parte 1', max_length=18)
    parte1_endereco = models.TextField('Endereço da Parte 1')
    
    parte2_nome = models.CharField('Nome da Parte 2', max_length=200)
    parte2_cpf_cnpj = models.CharField('CPF/CNPJ da Parte 2', max_length=18)
    parte2_endereco = models.TextField('Endereço da Parte 2')
    
    # Dados do contrato
    objeto_contrato = models.TextField('Objeto do Contrato')
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=200)
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Fim', blank=True, null=True)
    prazo_vigencia = models.CharField('Prazo de Vigência', max_length=100)
    
    # Campos específicos por tipo de contrato (JSON)
    dados_especificos = models.JSONField('Dados Específicos', default=dict, blank=True)
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.contract_type.name} - {self.parte1_nome} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('contracts:contract_detail', kwargs={'pk': self.pk})


class Payment(models.Model):
    """Pagamentos dos contratos"""
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('approved', 'Aprovado'),
        ('cancelled', 'Cancelado'),
        ('failed', 'Falhou'),
    ]
    
    PAYMENT_METHODS = [
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
    ]
    
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, verbose_name='Contrato')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField('Método de Pagamento', max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    transaction_id = models.CharField('ID da Transação', max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField('Data do Pagamento', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pagamento {self.contract} - {self.get_status_display()}"
