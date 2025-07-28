from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Choices para estados brasileiros
ESTADO_CHOICES = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]

ESTADO_CIVIL_CHOICES = [
    ('solteiro', 'Solteiro(a)'),
    ('casado', 'Casado(a)'),
    ('divorciado', 'Divorciado(a)'),
    ('viuvo', 'Viúvo(a)'),
    ('uniao_estavel', 'União Estável')
]

TIPO_IMOVEL_CHOICES = [
    ('apartamento', 'Apartamento'),
    ('casa', 'Casa'),
    ('chacara', 'Chácara'),
    ('cobertura', 'Cobertura'),
    ('duplex', 'Duplex'),
    ('fazenda', 'Fazenda'),
    ('flat', 'Flat'),
    ('galpao', 'Galpão'),
    ('kitnet', 'Kitnet'),
    ('loft', 'Loft'),
    ('mansao', 'Mansão'),
    ('sitio', 'Sítio'),
    ('sobrado', 'Sobrado'),
    ('studio', 'Studio'),
    ('terreno', 'Terreno')
]

FORMA_PAGAMENTO_CHOICES = [
    ('a_vista', 'À Vista'),
    ('parcelado', 'Parcelado'),
    ('financiado', 'Financiado')
]

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


class CompraVendaImovel(models.Model):
    """Modelo específico para contratos de compra e venda de imóvel"""
    
    # Relacionamento
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    
    # === DADOS DO PROPRIETÁRIO ===
    proprietario_nome = models.CharField('Nome Completo', max_length=200)
    proprietario_estado_civil = models.CharField('Estado Civil', max_length=20, choices=ESTADO_CIVIL_CHOICES)
    proprietario_nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Brasileira')
    proprietario_profissao = models.CharField('Profissão', max_length=100)
    proprietario_rg = models.CharField('RG', max_length=20)
    proprietario_cpf = models.CharField('CPF', max_length=14)
    
    # Endereço do proprietário
    proprietario_rua = models.CharField('Rua', max_length=200)
    proprietario_numero = models.CharField('Número', max_length=10)
    proprietario_bairro = models.CharField('Bairro', max_length=100)
    proprietario_cidade = models.CharField('Cidade', max_length=100)
    proprietario_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    proprietario_cep = models.CharField('CEP', max_length=9, blank=True)
    
    # Dados do cônjuge (se casado)
    proprietario_conjuge_nome = models.CharField('Nome do Cônjuge', max_length=200, blank=True)
    proprietario_conjuge_nacionalidade = models.CharField('Nacionalidade do Cônjuge', max_length=100, blank=True)
    proprietario_conjuge_profissao = models.CharField('Profissão do Cônjuge', max_length=100, blank=True)
    proprietario_conjuge_rg = models.CharField('RG do Cônjuge', max_length=20, blank=True)
    proprietario_conjuge_cpf = models.CharField('CPF do Cônjuge', max_length=14, blank=True)
    
    # === DADOS DO COMPRADOR ===
    comprador_nome = models.CharField('Nome Completo', max_length=200)
    comprador_estado_civil = models.CharField('Estado Civil', max_length=20, choices=ESTADO_CIVIL_CHOICES)
    comprador_nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Brasileira')
    comprador_profissao = models.CharField('Profissão', max_length=100)
    comprador_rg = models.CharField('RG', max_length=20)
    comprador_cpf = models.CharField('CPF', max_length=14)
    
    # Endereço do comprador
    comprador_rua = models.CharField('Rua', max_length=200)
    comprador_numero = models.CharField('Número', max_length=10)
    comprador_bairro = models.CharField('Bairro', max_length=100)
    comprador_cidade = models.CharField('Cidade', max_length=100)
    comprador_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    comprador_cep = models.CharField('CEP', max_length=9, blank=True)
    
    # Dados do cônjuge (se casado)
    comprador_conjuge_nome = models.CharField('Nome do Cônjuge', max_length=200, blank=True)
    comprador_conjuge_nacionalidade = models.CharField('Nacionalidade do Cônjuge', max_length=100, blank=True)
    comprador_conjuge_profissao = models.CharField('Profissão do Cônjuge', max_length=100, blank=True)
    comprador_conjuge_rg = models.CharField('RG do Cônjuge', max_length=20, blank=True)
    comprador_conjuge_cpf = models.CharField('CPF do Cônjuge', max_length=14, blank=True)
    
    # === DADOS DO IMÓVEL ===
    imovel_tipo = models.CharField('Tipo do Imóvel', max_length=20, choices=TIPO_IMOVEL_CHOICES)
    
    # Endereço do imóvel
    imovel_rua = models.CharField('Rua', max_length=200)
    imovel_numero = models.CharField('Número', max_length=10)
    imovel_bairro = models.CharField('Bairro', max_length=100)
    imovel_cidade = models.CharField('Cidade', max_length=100)
    imovel_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    imovel_cep = models.CharField('CEP', max_length=9, blank=True)
    
    # Dados registrais do imóvel
    imovel_matricula = models.CharField('Número da Matrícula', max_length=50)
    imovel_cartorio = models.CharField('Cartório de Registro', max_length=200)
    imovel_iptu = models.CharField('Número do IPTU', max_length=50)
    imovel_area_territorial = models.CharField('Área Territorial (m²)', max_length=20)
    imovel_area_construida = models.CharField('Área Construída (m²)', max_length=20, blank=True)
    
    # === DETALHES DA VENDA ===
    valor_total = models.DecimalField('Valor Total da Venda', max_digits=12, decimal_places=2)
    valor_extenso = models.TextField('Valor por Extenso')
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    data_pagamento = models.DateField('Data de Pagamento')
    conta_bancaria = models.CharField('Conta Bancária para Transferência', max_length=200, blank=True)
    
    # Dados específicos para pagamento parcelado
    quantidade_parcelas = models.PositiveIntegerField('Quantidade de Parcelas', blank=True, null=True)
    datas_parcelas = models.JSONField('Datas das Parcelas', default=list, blank=True)
    
    # Data de entrega
    data_entrega = models.DateField('Data de Entrega do Imóvel')
    
    # Status e metadados
    status = models.CharField('Status', max_length=20, choices=[
        ('rascunho', 'Rascunho'),
        ('finalizado', 'Finalizado'),
        ('assinado', 'Assinado'),
    ], default='rascunho')
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Contrato de Compra e Venda de Imóvel'
        verbose_name_plural = 'Contratos de Compra e Venda de Imóveis'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Compra/Venda - {self.proprietario_nome} → {self.comprador_nome} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('contracts:compra_venda_detail', kwargs={'pk': self.pk})


class ContratoCompraVendaImovel(models.Model):
    """Modelo completo para contrato de compra e venda de imóvel"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    
    # === DADOS DO PROPRIETÁRIO ===
    proprietario_nome = models.CharField('Nome Completo do Proprietário', max_length=200)
    proprietario_estado_civil = models.CharField('Estado Civil', max_length=20, choices=ESTADO_CIVIL_CHOICES)
    proprietario_nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Brasileira')
    proprietario_profissao = models.CharField('Profissão', max_length=100)
    proprietario_rg = models.CharField('RG', max_length=20)
    proprietario_cpf = models.CharField('CPF', max_length=14)
    
    # Endereço do proprietário
    proprietario_endereco_rua = models.CharField('Rua', max_length=200)
    proprietario_endereco_numero = models.CharField('Número', max_length=20)
    proprietario_endereco_bairro = models.CharField('Bairro', max_length=100)
    proprietario_endereco_cidade = models.CharField('Cidade', max_length=100)
    proprietario_endereco_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    proprietario_endereco_cep = models.CharField('CEP', max_length=9, blank=True)
    
    # Dados do cônjuge (se casado)
    proprietario_conjuge_nome = models.CharField('Nome do Cônjuge', max_length=200, blank=True)
    proprietario_conjuge_nacionalidade = models.CharField('Nacionalidade do Cônjuge', max_length=100, blank=True)
    proprietario_conjuge_profissao = models.CharField('Profissão do Cônjuge', max_length=100, blank=True)
    proprietario_conjuge_rg = models.CharField('RG do Cônjuge', max_length=20, blank=True)
    proprietario_conjuge_cpf = models.CharField('CPF do Cônjuge', max_length=14, blank=True)
    
    # === DADOS DO COMPRADOR ===
    comprador_nome = models.CharField('Nome Completo do Comprador', max_length=200)
    comprador_estado_civil = models.CharField('Estado Civil', max_length=20, choices=ESTADO_CIVIL_CHOICES)
    comprador_nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Brasileira')
    comprador_profissao = models.CharField('Profissão', max_length=100)
    comprador_rg = models.CharField('RG', max_length=20)
    comprador_cpf = models.CharField('CPF', max_length=14)
    
    # Endereço do comprador
    comprador_endereco_rua = models.CharField('Rua', max_length=200)
    comprador_endereco_numero = models.CharField('Número', max_length=20)
    comprador_endereco_bairro = models.CharField('Bairro', max_length=100)
    comprador_endereco_cidade = models.CharField('Cidade', max_length=100)
    comprador_endereco_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    comprador_endereco_cep = models.CharField('CEP', max_length=9, blank=True)
    
    # Dados do cônjuge (se casado)
    comprador_conjuge_nome = models.CharField('Nome do Cônjuge', max_length=200, blank=True)
    comprador_conjuge_nacionalidade = models.CharField('Nacionalidade do Cônjuge', max_length=100, blank=True)
    comprador_conjuge_profissao = models.CharField('Profissão do Cônjuge', max_length=100, blank=True)
    comprador_conjuge_rg = models.CharField('RG do Cônjuge', max_length=20, blank=True)
    comprador_conjuge_cpf = models.CharField('CPF do Cônjuge', max_length=14, blank=True)
    
    # === DADOS DO IMÓVEL ===
    imovel_tipo = models.CharField('Tipo do Imóvel', max_length=20, choices=TIPO_IMOVEL_CHOICES)
    
    # Endereço do imóvel
    imovel_endereco_rua = models.CharField('Rua', max_length=200)
    imovel_endereco_numero = models.CharField('Número', max_length=20)
    imovel_endereco_bairro = models.CharField('Bairro', max_length=100)
    imovel_endereco_cidade = models.CharField('Cidade', max_length=100)
    imovel_endereco_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    imovel_endereco_cep = models.CharField('CEP', max_length=9, blank=True)
    
    # Dados cartoriais e fiscais
    imovel_matricula = models.CharField('Número da Matrícula', max_length=50)
    imovel_cartorio = models.CharField('Cartório de Registro', max_length=200)
    imovel_iptu = models.CharField('Número do IPTU', max_length=50)
    imovel_area_territorial = models.CharField('Área Territorial (m²)', max_length=20)
    imovel_area_construida = models.CharField('Área Construída (m²)', max_length=20, blank=True)
    
    # === DETALHES DA VENDA ===
    valor_total = models.DecimalField('Valor Total da Venda', max_digits=12, decimal_places=2)
    valor_extenso = models.TextField('Valor por Extenso')
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    data_pagamento = models.DateField('Data de Pagamento')
    conta_bancaria = models.CharField('Conta Bancária para Transferência', max_length=200, blank=True)
    
    # Dados específicos para pagamento parcelado
    quantidade_parcelas = models.PositiveIntegerField('Quantidade de Parcelas', blank=True, null=True)
    datas_parcelas = models.JSONField('Datas das Parcelas', default=list, blank=True)
    
    # Data de entrega
    data_entrega = models.DateField('Data de Entrega do Imóvel')
    
    # Status e metadados
    status = models.CharField('Status', max_length=20, choices=[
        ('rascunho', 'Rascunho'),
        ('finalizado', 'Finalizado'),
        ('assinado', 'Assinado'),
    ], default='rascunho')
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Contrato de Compra e Venda de Imóvel Completo'
        verbose_name_plural = 'Contratos de Compra e Venda de Imóveis Completos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Compra/Venda - {self.proprietario_nome} → {self.comprador_nome} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('contracts:compra_venda_detail_completo', kwargs={'pk': self.pk})
    
    @property
    def endereco_completo_proprietario(self):
        return f"{self.proprietario_endereco_rua}, {self.proprietario_endereco_numero}, {self.proprietario_endereco_bairro}, {self.proprietario_endereco_cidade}/{self.proprietario_endereco_estado}"
    
    @property
    def endereco_completo_comprador(self):
        return f"{self.comprador_endereco_rua}, {self.comprador_endereco_numero}, {self.comprador_endereco_bairro}, {self.comprador_endereco_cidade}/{self.comprador_endereco_estado}"
    
    @property
    def endereco_completo_imovel(self):
        return f"{self.imovel_endereco_rua}, {self.imovel_endereco_numero}, {self.imovel_endereco_bairro}, {self.imovel_endereco_cidade}/{self.imovel_endereco_estado}"


class ContratoLocacaoResidencial(models.Model):
    """Modelo para contratos de locação residencial completos"""
    
    # Opções para formulários
    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro'),
        ('casado', 'Casado'),
        ('divorciado', 'Divorciado'),
        ('viuvo', 'Viúvo'),
        ('uniao_estavel', 'União Estável'),
    ]
    
    ESTADO_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]
    
    TIPO_IMOVEL_CHOICES = [
        ('apartamento', 'Apartamento'),
        ('casa', 'Casa'),
        ('chacara', 'Chácara'),
        ('cobertura', 'Cobertura'),
        ('duplex', 'Duplex'),
        ('fazenda', 'Fazenda'),
        ('flat', 'Flat'),
        ('galpao', 'Galpão'),
        ('kitnet', 'Kitnet'),
        ('loft', 'Loft'),
        ('mansao', 'Mansão'),
        ('sitio', 'Sítio'),
        ('sobrado', 'Sobrado'),
        ('studio', 'Studio'),
        ('terreno', 'Terreno'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('boleto', 'Boleto'),
        ('pix', 'PIX'),
        ('transferencia', 'Transferência Bancária'),
    ]
    
    DIA_PAGAMENTO_CHOICES = [
        (str(i), f"Dia {i}") for i in range(1, 32)
    ]
    
    GARANTIA_CHOICES = [
        ('caucao', 'Caução'),
        ('fiador', 'Fiador/Avalista'),
        ('seguro', 'Seguro Fiança'),
    ]
    
    # Campos básicos
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Usuário')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    # === DADOS DO PROPRIETÁRIO ===
    proprietario_nome = models.CharField('Nome Completo', max_length=200)
    proprietario_estado_civil = models.CharField('Estado Civil', max_length=20, choices=ESTADO_CIVIL_CHOICES)
    proprietario_nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Brasileira')
    proprietario_profissao = models.CharField('Profissão', max_length=100)
    proprietario_rg = models.CharField('RG', max_length=20)
    proprietario_cpf = models.CharField('CPF', max_length=14)
    
    # Endereço do proprietário
    proprietario_rua = models.CharField('Rua', max_length=200)
    proprietario_numero = models.CharField('Número', max_length=10)
    proprietario_bairro = models.CharField('Bairro', max_length=100)
    proprietario_cidade = models.CharField('Cidade', max_length=100)
    proprietario_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    
    # Dados do cônjuge (se casado)
    proprietario_conjuge_nome = models.CharField('Nome do Cônjuge', max_length=200, blank=True)
    proprietario_conjuge_nacionalidade = models.CharField('Nacionalidade do Cônjuge', max_length=100, blank=True)
    proprietario_conjuge_profissao = models.CharField('Profissão do Cônjuge', max_length=100, blank=True)
    proprietario_conjuge_rg = models.CharField('RG do Cônjuge', max_length=20, blank=True)
    proprietario_conjuge_cpf = models.CharField('CPF do Cônjuge', max_length=14, blank=True)
    
    # === DADOS DO LOCATÁRIO ===
    locatario_nome = models.CharField('Nome Completo', max_length=200)
    locatario_estado_civil = models.CharField('Estado Civil', max_length=20, choices=ESTADO_CIVIL_CHOICES)
    locatario_nacionalidade = models.CharField('Nacionalidade', max_length=100, default='Brasileira')
    locatario_profissao = models.CharField('Profissão', max_length=100)
    locatario_rg = models.CharField('RG', max_length=20)
    locatario_cpf = models.CharField('CPF', max_length=14)
    
    # Endereço do locatário
    locatario_rua = models.CharField('Rua', max_length=200)
    locatario_numero = models.CharField('Número', max_length=10)
    locatario_bairro = models.CharField('Bairro', max_length=100)
    locatario_cidade = models.CharField('Cidade', max_length=100)
    locatario_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    
    # Dados do cônjuge (se casado)
    locatario_conjuge_nome = models.CharField('Nome do Cônjuge', max_length=200, blank=True)
    locatario_conjuge_nacionalidade = models.CharField('Nacionalidade do Cônjuge', max_length=100, blank=True)
    locatario_conjuge_profissao = models.CharField('Profissão do Cônjuge', max_length=100, blank=True)
    locatario_conjuge_rg = models.CharField('RG do Cônjuge', max_length=20, blank=True)
    locatario_conjuge_cpf = models.CharField('CPF do Cônjuge', max_length=14, blank=True)
    
    # === DADOS DO IMÓVEL ===
    imovel_tipo = models.CharField('Tipo do Imóvel', max_length=20, choices=TIPO_IMOVEL_CHOICES)
    
    # Endereço do imóvel
    imovel_rua = models.CharField('Rua', max_length=200)
    imovel_numero = models.CharField('Número', max_length=10)
    imovel_bairro = models.CharField('Bairro', max_length=100)
    imovel_cidade = models.CharField('Cidade', max_length=100)
    imovel_estado = models.CharField('Estado', max_length=2, choices=ESTADO_CHOICES)
    
    # Dados registrais do imóvel (opcionais)
    imovel_matricula = models.CharField('Número da Matrícula', max_length=50, blank=True)
    imovel_cartorio = models.CharField('Cartório onde foi Registrado', max_length=200, blank=True)
    imovel_iptu = models.CharField('Número do IPTU', max_length=50, blank=True)
    imovel_conta_agua = models.CharField('Número da Conta de Água', max_length=50, blank=True)
    imovel_conta_luz = models.CharField('Número da Conta de Luz', max_length=50, blank=True)
    
    # === DETALHES DA LOCAÇÃO ===
    valor_aluguel = models.DecimalField('Valor do Aluguel', max_digits=12, decimal_places=2)
    valor_aluguel_extenso = models.CharField('Valor por Extenso', max_length=500)
    forma_pagamento = models.CharField('Forma de Pagamento', max_length=20, choices=FORMA_PAGAMENTO_CHOICES)
    dia_pagamento = models.CharField('Dia de Pagamento', max_length=2, choices=DIA_PAGAMENTO_CHOICES)
    conta_bancaria = models.CharField('Conta Bancária para Transferência', max_length=200, blank=True)
    
    # Datas da locação
    data_inicio = models.DateField('Data de Início da Locação')
    data_termino = models.DateField('Data de Término da Locação')
    
    # Garantia da locação
    tipo_garantia = models.CharField('Tipo de Garantia', max_length=20, choices=GARANTIA_CHOICES)
    
    # Caução (se aplicável)
    valor_caucao = models.DecimalField('Valor da Caução', max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Fiador (se aplicável)
    fiador_nome = models.CharField('Nome do Fiador', max_length=200, blank=True)
    fiador_estado_civil = models.CharField('Estado Civil do Fiador', max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True)
    fiador_nacionalidade = models.CharField('Nacionalidade do Fiador', max_length=100, blank=True)
    fiador_profissao = models.CharField('Profissão do Fiador', max_length=100, blank=True)
    fiador_rg = models.CharField('RG do Fiador', max_length=20, blank=True)
    fiador_cpf = models.CharField('CPF do Fiador', max_length=14, blank=True)
    
    # Endereço do fiador
    fiador_rua = models.CharField('Rua do Fiador', max_length=200, blank=True)
    fiador_numero = models.CharField('Número do Fiador', max_length=10, blank=True)
    fiador_bairro = models.CharField('Bairro do Fiador', max_length=100, blank=True)
    fiador_cidade = models.CharField('Cidade do Fiador', max_length=100, blank=True)
    fiador_estado = models.CharField('Estado do Fiador', max_length=2, choices=ESTADO_CHOICES, blank=True)
    
    # Seguro Fiança (se aplicável)
    seguro_nome_seguradora = models.CharField('Nome da Seguradora', max_length=200, blank=True)
    seguro_prazo = models.CharField('Prazo do Seguro', max_length=100, blank=True)
    seguro_valor = models.DecimalField('Valor do Seguro', max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Observações
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        verbose_name = 'Contrato de Locação Residencial'
        verbose_name_plural = 'Contratos de Locação Residencial'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Locação - {self.proprietario_nome} → {self.locatario_nome} - {self.created_at.strftime('%d/%m/%Y')}"
    
    def get_absolute_url(self):
        return reverse('contracts:locacao_residencial_detail', kwargs={'pk': self.pk})
    
    @property
    def endereco_completo_proprietario(self):
        return f"{self.proprietario_rua}, {self.proprietario_numero}, {self.proprietario_bairro}, {self.proprietario_cidade}/{self.proprietario_estado}"
    
    @property
    def endereco_completo_locatario(self):
        return f"{self.locatario_rua}, {self.locatario_numero}, {self.locatario_bairro}, {self.locatario_cidade}/{self.locatario_estado}"
    
    @property
    def endereco_completo_imovel(self):
        return f"{self.imovel_rua}, {self.imovel_numero}, {self.imovel_bairro}, {self.imovel_cidade}/{self.imovel_estado}"
    
    @property
    def endereco_completo_fiador(self):
        if self.fiador_rua:
            return f"{self.fiador_rua}, {self.fiador_numero}, {self.fiador_bairro}, {self.fiador_cidade}/{self.fiador_estado}"
        return ""
