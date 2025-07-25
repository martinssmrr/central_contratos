from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Row, Column, Div
import re
from .models import Contract, CompraVendaImovel, ContratoCompraVendaImovel, ESTADO_CHOICES, ESTADO_CIVIL_CHOICES, TIPO_IMOVEL_CHOICES, FORMA_PAGAMENTO_CHOICES

class ContractForm(ModelForm):
    """Formulário base para criação de contratos"""
    
    class Meta:
        model = Contract
        fields = [
            'parte1_nome', 'parte1_cpf_cnpj', 'parte1_endereco',
            'parte2_nome', 'parte2_cpf_cnpj', 'parte2_endereco',
            'objeto_contrato', 'valor', 'forma_pagamento',
            'data_inicio', 'data_fim', 'prazo_vigencia'
        ]
        widgets = {
            'parte1_endereco': forms.Textarea(attrs={'rows': 3}),
            'parte2_endereco': forms.Textarea(attrs={'rows': 3}),
            'objeto_contrato': forms.Textarea(attrs={'rows': 4}),
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Dados da Primeira Parte (Contratante)',
                Row(
                    Column('parte1_nome', css_class='form-group col-md-8 mb-0'),
                    Column('parte1_cpf_cnpj', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                'parte1_endereco',
            ),
            Fieldset(
                'Dados da Segunda Parte (Contratado)',
                Row(
                    Column('parte2_nome', css_class='form-group col-md-8 mb-0'),
                    Column('parte2_cpf_cnpj', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                'parte2_endereco',
            ),
            Fieldset(
                'Dados do Contrato',
                'objeto_contrato',
                Row(
                    Column('valor', css_class='form-group col-md-6 mb-0'),
                    Column('forma_pagamento', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('data_inicio', css_class='form-group col-md-4 mb-0'),
                    Column('data_fim', css_class='form-group col-md-4 mb-0'),
                    Column('prazo_vigencia', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
            ),
            Submit('submit', 'Gerar Contrato', css_class='btn btn-primary btn-lg')
        )


class PrestacaoServicoForm(ContractForm):
    """Formulário específico para prestação de serviços"""
    servicos_detalhados = forms.CharField(
        label='Serviços Detalhados',
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Descreva detalhadamente os serviços a serem prestados'
    )
    local_prestacao = forms.CharField(
        label='Local de Prestação',
        max_length=200,
        help_text='Onde os serviços serão realizados'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar campos específicos ao layout
        self.helper.layout[2].fields.extend(['servicos_detalhados', 'local_prestacao'])


class LocacaoForm(ContractForm):
    """Formulário para contratos de locação"""
    endereco_imovel = forms.CharField(
        label='Endereço do Imóvel',
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Endereço completo do imóvel a ser locado'
    )
    valor_caucao = forms.DecimalField(
        label='Valor da Caução',
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    )
    dia_vencimento = forms.IntegerField(
        label='Dia do Vencimento',
        min_value=1,
        max_value=31,
        help_text='Dia do mês para vencimento do aluguel'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout[2].fields.extend(['endereco_imovel', 'valor_caucao', 'dia_vencimento'])


class CompraVendaForm(ContractForm):
    """Formulário para contratos de compra e venda"""
    descricao_bem = forms.CharField(
        label='Descrição do Bem',
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Descreva detalhadamente o bem a ser vendido'
    )
    local_entrega = forms.CharField(
        label='Local de Entrega',
        max_length=200,
        help_text='Onde o bem será entregue'
    )
    prazo_entrega = forms.CharField(
        label='Prazo de Entrega',
        max_length=100,
        help_text='Prazo para entrega do bem'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout[2].fields.extend(['descricao_bem', 'local_entrega', 'prazo_entrega'])


class ConfissaoDividaForm(ContractForm):
    """Formulário para confissão de dívida"""
    origem_divida = forms.CharField(
        label='Origem da Dívida',
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Como a dívida foi originada'
    )
    valor_juros = forms.DecimalField(
        label='Valor dos Juros (%)',
        max_digits=5,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'})
    )
    data_vencimento = forms.DateField(
        label='Data de Vencimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout[2].fields.extend(['origem_divida', 'valor_juros', 'data_vencimento'])


class FreelancerForm(ContractForm):
    """Formulário para contratos de freelancer"""
    projeto_detalhado = forms.CharField(
        label='Descrição Detalhada do Projeto',
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text='Descreva o projeto e todas as entregas esperadas'
    )
    prazo_entrega = forms.CharField(
        label='Prazo de Entrega',
        max_length=100,
        help_text='Prazo para conclusão do projeto'
    )
    direitos_autorais = forms.ChoiceField(
        label='Direitos Autorais',
        choices=[
            ('cliente', 'Transferidos ao Cliente'),
            ('freelancer', 'Mantidos pelo Freelancer'),
            ('compartilhados', 'Compartilhados')
        ],
        widget=forms.RadioSelect
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout[2].fields.extend(['projeto_detalhado', 'prazo_entrega', 'direitos_autorais'])


class PaymentForm(forms.Form):
    """Formulário para processamento de pagamento"""
    payment_method = forms.ChoiceField(
        label='Método de Pagamento',
        choices=[
            ('credit_card', 'Cartão de Crédito'),
            ('debit_card', 'Cartão de Débito'),
            ('pix', 'PIX'),
            ('boleto', 'Boleto Bancário'),
        ],
        widget=forms.RadioSelect
    )
    
    # Campos para cartão (opcional, dependendo do método)
    card_number = forms.CharField(
        label='Número do Cartão',
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '0000 0000 0000 0000'})
    )
    card_name = forms.CharField(
        label='Nome no Cartão',
        max_length=100,
        required=False
    )
    card_expiry = forms.CharField(
        label='Validade',
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'MM/AA'})
    )
    card_cvv = forms.CharField(
        label='CVV',
        max_length=4,
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '000'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'payment_method',
            HTML('<div id="card-fields" style="display: none;">'),
            'card_number',
            Row(
                Column('card_name', css_class='form-group col-md-6 mb-0'),
                Column('card_expiry', css_class='form-group col-md-3 mb-0'),
                Column('card_cvv', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            HTML('</div>'),
            Submit('submit', 'Processar Pagamento', css_class='btn btn-success btn-lg')
        )


class CompraVendaImovelForm(ModelForm):
    """Formulário para contrato de compra e venda de imóvel"""
    
    class Meta:
        model = CompraVendaImovel
        exclude = ['user', 'created_at', 'updated_at', 'status']
        
        widgets = {
            # Campos de data
            'data_pagamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            # Campos de valor
            'valor_total': forms.NumberInput(attrs={
                'step': '0.01', 
                'min': '0', 
                'class': 'form-control',
                'placeholder': 'Ex: 500000.00'
            }),
            
            # Área de texto
            'valor_extenso': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Quinhentos mil reais'
            }),
            
            # Campos de texto normais
            'proprietario_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12.345.678-9'}),
            'proprietario_cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            
            # Endereço proprietário
            'proprietario_rua': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12345-678'}),
            
            # Cônjuge proprietário
            'proprietario_conjuge_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_conjuge_nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_conjuge_profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_conjuge_rg': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietario_conjuge_cpf': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Comprador
            'comprador_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_rg': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_cpf': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Endereço comprador
            'comprador_rua': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_cep': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Cônjuge comprador
            'comprador_conjuge_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_conjuge_nacionalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_conjuge_profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_conjuge_rg': forms.TextInput(attrs={'class': 'form-control'}),
            'comprador_conjuge_cpf': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Imóvel
            'imovel_rua': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_numero': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_cep': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_cartorio': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_iptu': forms.TextInput(attrs={'class': 'form-control'}),
            'imovel_area_territorial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 250.50'}),
            'imovel_area_construida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 180.25'}),
            
            # Venda
            'conta_bancaria': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_parcelas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            
            # Selects
            'proprietario_estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'proprietario_estado': forms.Select(attrs={'class': 'form-select'}),
            'comprador_estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'comprador_estado': forms.Select(attrs={'class': 'form-select'}),
            'imovel_tipo': forms.Select(attrs={'class': 'form-select'}),
            'imovel_estado': forms.Select(attrs={'class': 'form-select'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
        }
        
        labels = {
            # Proprietário
            'proprietario_nome': 'Nome Completo',
            'proprietario_estado_civil': 'Estado Civil',
            'proprietario_nacionalidade': 'Nacionalidade',
            'proprietario_profissao': 'Profissão',
            'proprietario_rg': 'RG',
            'proprietario_cpf': 'CPF',
            'proprietario_rua': 'Rua/Avenida',
            'proprietario_numero': 'Número',
            'proprietario_bairro': 'Bairro',
            'proprietario_cidade': 'Cidade',
            'proprietario_estado': 'Estado',
            'proprietario_cep': 'CEP',
            
            # Cônjuge proprietário
            'proprietario_conjuge_nome': 'Nome Completo do Cônjuge',
            'proprietario_conjuge_nacionalidade': 'Nacionalidade',
            'proprietario_conjuge_profissao': 'Profissão',
            'proprietario_conjuge_rg': 'RG',
            'proprietario_conjuge_cpf': 'CPF',
            
            # Comprador
            'comprador_nome': 'Nome Completo',
            'comprador_estado_civil': 'Estado Civil',
            'comprador_nacionalidade': 'Nacionalidade',
            'comprador_profissao': 'Profissão',
            'comprador_rg': 'RG',
            'comprador_cpf': 'CPF',
            'comprador_rua': 'Rua/Avenida',
            'comprador_numero': 'Número',
            'comprador_bairro': 'Bairro',
            'comprador_cidade': 'Cidade',
            'comprador_estado': 'Estado',
            'comprador_cep': 'CEP',
            
            # Cônjuge comprador
            'comprador_conjuge_nome': 'Nome Completo do Cônjuge',
            'comprador_conjuge_nacionalidade': 'Nacionalidade',
            'comprador_conjuge_profissao': 'Profissão',
            'comprador_conjuge_rg': 'RG',
            'comprador_conjuge_cpf': 'CPF',
            
            # Imóvel
            'imovel_tipo': 'Tipo do Imóvel',
            'imovel_rua': 'Rua/Avenida',
            'imovel_numero': 'Número',
            'imovel_bairro': 'Bairro',
            'imovel_cidade': 'Cidade',
            'imovel_estado': 'Estado',
            'imovel_cep': 'CEP',
            'imovel_matricula': 'Número da Matrícula',
            'imovel_cartorio': 'Cartório de Registro',
            'imovel_iptu': 'Número do IPTU',
            'imovel_area_territorial': 'Área Territorial (m²)',
            'imovel_area_construida': 'Área Construída (m²)',
            
            # Venda
            'valor_total': 'Valor Total da Venda',
            'valor_extenso': 'Valor por Extenso',
            'forma_pagamento': 'Forma de Pagamento',
            'data_pagamento': 'Data de Pagamento',
            'conta_bancaria': 'Conta Bancária para Transferência',
            'quantidade_parcelas': 'Quantidade de Parcelas',
            'data_entrega': 'Data de Entrega do Imóvel',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'compra-venda-form'
        
        self.helper.layout = Layout(
            HTML('<div class="form-header mb-4"><h2><i class="fas fa-home me-2"></i>Contrato de Compra e Venda de Imóvel</h2></div>'),
            
            # Seção Proprietário
            Fieldset(
                '<i class="fas fa-user-tie me-2"></i>Dados do Proprietário',
                Row(
                    Column('proprietario_nome', css_class='form-group col-md-8'),
                    Column('proprietario_estado_civil', css_class='form-group col-md-4'),
                ),
                Row(
                    Column('proprietario_nacionalidade', css_class='form-group col-md-4'),
                    Column('proprietario_profissao', css_class='form-group col-md-4'),
                    Column('proprietario_rg', css_class='form-group col-md-2'),
                    Column('proprietario_cpf', css_class='form-group col-md-2'),
                ),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-map-marker-alt me-2"></i>Endereço do Proprietário</h6>'),
                Row(
                    Column('proprietario_rua', css_class='form-group col-md-6'),
                    Column('proprietario_numero', css_class='form-group col-md-2'),
                    Column('proprietario_bairro', css_class='form-group col-md-4'),
                ),
                Row(
                    Column('proprietario_cidade', css_class='form-group col-md-5'),
                    Column('proprietario_estado', css_class='form-group col-md-2'),
                    Column('proprietario_cep', css_class='form-group col-md-2'),
                ),
                
                # Dados do cônjuge (proprietário)
                HTML('<div id="proprietario-conjuge-section" style="display: none;">'),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-heart me-2"></i>Dados do Cônjuge</h6>'),
                Row(
                    Column('proprietario_conjuge_nome', css_class='form-group col-md-6'),
                    Column('proprietario_conjuge_nacionalidade', css_class='form-group col-md-3'),
                    Column('proprietario_conjuge_profissao', css_class='form-group col-md-3'),
                ),
                Row(
                    Column('proprietario_conjuge_rg', css_class='form-group col-md-3'),
                    Column('proprietario_conjuge_cpf', css_class='form-group col-md-3'),
                ),
                HTML('</div>'),
                css_class='card-section'
            ),
            
            # Seção Comprador
            Fieldset(
                '<i class="fas fa-user-check me-2"></i>Dados do Comprador',
                Row(
                    Column('comprador_nome', css_class='form-group col-md-8'),
                    Column('comprador_estado_civil', css_class='form-group col-md-4'),
                ),
                Row(
                    Column('comprador_nacionalidade', css_class='form-group col-md-4'),
                    Column('comprador_profissao', css_class='form-group col-md-4'),
                    Column('comprador_rg', css_class='form-group col-md-2'),
                    Column('comprador_cpf', css_class='form-group col-md-2'),
                ),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-map-marker-alt me-2"></i>Endereço do Comprador</h6>'),
                Row(
                    Column('comprador_rua', css_class='form-group col-md-6'),
                    Column('comprador_numero', css_class='form-group col-md-2'),
                    Column('comprador_bairro', css_class='form-group col-md-4'),
                ),
                Row(
                    Column('comprador_cidade', css_class='form-group col-md-5'),
                    Column('comprador_estado', css_class='form-group col-md-2'),
                    Column('comprador_cep', css_class='form-group col-md-2'),
                ),
                
                # Dados do cônjuge (comprador)
                HTML('<div id="comprador-conjuge-section" style="display: none;">'),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-heart me-2"></i>Dados do Cônjuge</h6>'),
                Row(
                    Column('comprador_conjuge_nome', css_class='form-group col-md-6'),
                    Column('comprador_conjuge_nacionalidade', css_class='form-group col-md-3'),
                    Column('comprador_conjuge_profissao', css_class='form-group col-md-3'),
                ),
                Row(
                    Column('comprador_conjuge_rg', css_class='form-group col-md-3'),
                    Column('comprador_conjuge_cpf', css_class='form-group col-md-3'),
                ),
                HTML('</div>'),
                css_class='card-section'
            ),
            
            # Seção Imóvel
            Fieldset(
                '<i class="fas fa-home me-2"></i>Dados do Imóvel',
                Row(
                    Column('imovel_tipo', css_class='form-group col-md-4'),
                ),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-map-marker-alt me-2"></i>Localização do Imóvel</h6>'),
                Row(
                    Column('imovel_rua', css_class='form-group col-md-6'),
                    Column('imovel_numero', css_class='form-group col-md-2'),
                    Column('imovel_bairro', css_class='form-group col-md-4'),
                ),
                Row(
                    Column('imovel_cidade', css_class='form-group col-md-5'),
                    Column('imovel_estado', css_class='form-group col-md-2'),
                    Column('imovel_cep', css_class='form-group col-md-2'),
                ),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-file-alt me-2"></i>Dados Registrais</h6>'),
                Row(
                    Column('imovel_matricula', css_class='form-group col-md-4'),
                    Column('imovel_cartorio', css_class='form-group col-md-8'),
                ),
                Row(
                    Column('imovel_iptu', css_class='form-group col-md-4'),
                    Column('imovel_area_territorial', css_class='form-group col-md-4'),
                    Column('imovel_area_construida', css_class='form-group col-md-4'),
                ),
                css_class='card-section'
            ),
            
            # Seção Detalhes da Venda
            Fieldset(
                '<i class="fas fa-dollar-sign me-2"></i>Detalhes da Venda',
                Row(
                    Column('valor_total', css_class='form-group col-md-4'),
                    Column('forma_pagamento', css_class='form-group col-md-4'),
                    Column('data_pagamento', css_class='form-group col-md-4'),
                ),
                'valor_extenso',
                'conta_bancaria',
                
                # Campos condicionais para parcelamento
                HTML('<div id="parcelamento-section" style="display: none;">'),
                HTML('<h6 class="mt-3 mb-2"><i class="fas fa-calendar-alt me-2"></i>Detalhes do Parcelamento</h6>'),
                Row(
                    Column('quantidade_parcelas', css_class='form-group col-md-4'),
                ),
                HTML('<div id="datas-parcelas-container"></div>'),
                HTML('</div>'),
                
                Row(
                    Column('data_entrega', css_class='form-group col-md-4'),
                ),
                css_class='card-section'
            ),
            
            HTML('<div class="form-actions mt-4">'),
            Submit('submit', 'Gerar Contrato', css_class='btn btn-primary btn-lg me-3'),
            HTML('<button type="button" class="btn btn-outline-secondary btn-lg" onclick="history.back()">Cancelar</button>'),
            HTML('</div>')
        )
    
    def clean_proprietario_cpf(self):
        cpf = self.cleaned_data.get('proprietario_cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_comprador_cpf(self):
        cpf = self.cleaned_data.get('comprador_cpf')
        if cpf:
            # Remove caracteres não numéricos
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_valor_total(self):
        valor = self.cleaned_data.get('valor_total')
        if valor and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor


class ContratoCompraVendaImovelForm(ModelForm):
    """Formulário completo para contrato de compra e venda de imóvel"""
    
    class Meta:
        model = ContratoCompraVendaImovel
        exclude = ['user', 'status', 'created_at', 'updated_at']
        
        widgets = {
            # Datas
            'data_pagamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            
            # Valores monetários
            'valor_total': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'class': 'form-control'}),
            'valor_extenso': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Exemplo: Cem mil reais'}),
            
            # Campos de texto
            'proprietario_endereco_rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Rua das Flores'}),
            'proprietario_endereco_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123'}),
            'proprietario_endereco_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Centro'}),
            'proprietario_endereco_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),
            'proprietario_endereco_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            
            'comprador_endereco_rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Rua das Flores'}),
            'comprador_endereco_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123'}),
            'comprador_endereco_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Centro'}),
            'comprador_endereco_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),
            'comprador_endereco_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            
            'imovel_endereco_rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Rua das Flores'}),
            'imovel_endereco_numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123'}),
            'imovel_endereco_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Centro'}),
            'imovel_endereco_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo'}),
            'imovel_endereco_cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            
            # Campos específicos
            'proprietario_cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'}),
            'proprietario_rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000-0'}),
            'proprietario_conjuge_cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'}),
            'proprietario_conjuge_rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000-0'}),
            
            'comprador_cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'}),
            'comprador_rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000-0'}),
            'comprador_conjuge_cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'}),
            'comprador_conjuge_rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000-0'}),
            
            'imovel_area_territorial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 250.00'}),
            'imovel_area_construida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 180.00'}),
            
            'conta_bancaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Banco, Agência, Conta'}),
            'quantidade_parcelas': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '240'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS a todos os campos
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
                
        # Marcar campos obrigatórios
        required_fields = [
            'proprietario_nome', 'proprietario_estado_civil', 'proprietario_nacionalidade',
            'proprietario_profissao', 'proprietario_rg', 'proprietario_cpf',
            'proprietario_endereco_rua', 'proprietario_endereco_numero', 'proprietario_endereco_bairro',
            'proprietario_endereco_cidade', 'proprietario_endereco_estado',
            
            'comprador_nome', 'comprador_estado_civil', 'comprador_nacionalidade',
            'comprador_profissao', 'comprador_rg', 'comprador_cpf',
            'comprador_endereco_rua', 'comprador_endereco_numero', 'comprador_endereco_bairro',
            'comprador_endereco_cidade', 'comprador_endereco_estado',
            
            'imovel_tipo', 'imovel_endereco_rua', 'imovel_endereco_numero',
            'imovel_endereco_bairro', 'imovel_endereco_cidade', 'imovel_endereco_estado',
            'imovel_matricula', 'imovel_cartorio', 'imovel_iptu', 'imovel_area_territorial',
            
            'valor_total', 'valor_extenso', 'forma_pagamento', 'data_pagamento', 'data_entrega'
        ]
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
    
    def clean_proprietario_cpf(self):
        cpf = self.cleaned_data.get('proprietario_cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_comprador_cpf(self):
        cpf = self.cleaned_data.get('comprador_cpf')
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_proprietario_conjuge_cpf(self):
        estado_civil = self.cleaned_data.get('proprietario_estado_civil')
        cpf = self.cleaned_data.get('proprietario_conjuge_cpf')
        
        if estado_civil == 'casado' and not cpf:
            raise forms.ValidationError('CPF do cônjuge é obrigatório para pessoas casadas.')
        
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_comprador_conjuge_cpf(self):
        estado_civil = self.cleaned_data.get('comprador_estado_civil')
        cpf = self.cleaned_data.get('comprador_conjuge_cpf')
        
        if estado_civil == 'casado' and not cpf:
            raise forms.ValidationError('CPF do cônjuge é obrigatório para pessoas casadas.')
        
        if cpf:
            cpf = ''.join(filter(str.isdigit, cpf))
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_valor_total(self):
        valor = self.cleaned_data.get('valor_total')
        if valor and valor <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')
        return valor
    
    def clean_quantidade_parcelas(self):
        forma_pagamento = self.cleaned_data.get('forma_pagamento')
        quantidade_parcelas = self.cleaned_data.get('quantidade_parcelas')
        
        if forma_pagamento == 'parcelado' and not quantidade_parcelas:
            raise forms.ValidationError('Quantidade de parcelas é obrigatória para pagamento parcelado.')
        
        if quantidade_parcelas and quantidade_parcelas < 1:
            raise forms.ValidationError('Quantidade de parcelas deve ser maior que zero.')
        
        return quantidade_parcelas


class ContratoLocacaoResidencialForm(ModelForm):
    """Formulário para contratos de locação residencial"""
    
    class Meta:
        from .models import ContratoLocacaoResidencial
        model = ContratoLocacaoResidencial
        fields = [
            # Proprietário
            'proprietario_nome', 'proprietario_estado_civil', 'proprietario_nacionalidade',
            'proprietario_profissao', 'proprietario_rg', 'proprietario_cpf',
            'proprietario_rua', 'proprietario_numero', 'proprietario_bairro',
            'proprietario_cidade', 'proprietario_estado',
            'proprietario_conjuge_nome', 'proprietario_conjuge_nacionalidade',
            'proprietario_conjuge_profissao', 'proprietario_conjuge_rg', 'proprietario_conjuge_cpf',
            
            # Locatário
            'locatario_nome', 'locatario_estado_civil', 'locatario_nacionalidade',
            'locatario_profissao', 'locatario_rg', 'locatario_cpf',
            'locatario_rua', 'locatario_numero', 'locatario_bairro',
            'locatario_cidade', 'locatario_estado',
            'locatario_conjuge_nome', 'locatario_conjuge_nacionalidade',
            'locatario_conjuge_profissao', 'locatario_conjuge_rg', 'locatario_conjuge_cpf',
            
            # Imóvel
            'imovel_tipo', 'imovel_rua', 'imovel_numero', 'imovel_bairro',
            'imovel_cidade', 'imovel_estado', 'imovel_matricula', 'imovel_cartorio',
            'imovel_iptu', 'imovel_conta_agua', 'imovel_conta_luz',
            
            # Detalhes da locação
            'valor_aluguel', 'valor_aluguel_extenso', 'forma_pagamento',
            'dia_pagamento', 'conta_bancaria', 'data_inicio', 'data_termino',
            
            # Garantia
            'tipo_garantia', 'valor_caucao',
            'fiador_nome', 'fiador_estado_civil', 'fiador_nacionalidade',
            'fiador_profissao', 'fiador_rg', 'fiador_cpf',
            'fiador_rua', 'fiador_numero', 'fiador_bairro',
            'fiador_cidade', 'fiador_estado',
            'seguro_nome_seguradora', 'seguro_prazo', 'seguro_valor',
            
            # Observações
            'observacoes',
        ]
        
        widgets = {
            # Proprietário
            'proprietario_nome': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome completo do proprietário'
            }),
            'proprietario_estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'proprietario_nacionalidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: Brasileira'
            }),
            'proprietario_profissao': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Profissão'
            }),
            'proprietario_rg': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '00.000.000-0'
            }),
            'proprietario_cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'
            }),
            'proprietario_rua': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome da rua'
            }),
            'proprietario_numero': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número'
            }),
            'proprietario_bairro': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Bairro'
            }),
            'proprietario_cidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Cidade'
            }),
            'proprietario_estado': forms.Select(attrs={'class': 'form-select'}),
            
            # Cônjuge do proprietário
            'proprietario_conjuge_nome': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome completo do cônjuge'
            }),
            'proprietario_conjuge_nacionalidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: Brasileira'
            }),
            'proprietario_conjuge_profissao': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Profissão'
            }),
            'proprietario_conjuge_rg': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '00.000.000-0'
            }),
            'proprietario_conjuge_cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'
            }),
            
            # Locatário
            'locatario_nome': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome completo do locatário'
            }),
            'locatario_estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'locatario_nacionalidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: Brasileira'
            }),
            'locatario_profissao': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Profissão'
            }),
            'locatario_rg': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '00.000.000-0'
            }),
            'locatario_cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'
            }),
            'locatario_rua': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome da rua'
            }),
            'locatario_numero': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número'
            }),
            'locatario_bairro': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Bairro'
            }),
            'locatario_cidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Cidade'
            }),
            'locatario_estado': forms.Select(attrs={'class': 'form-select'}),
            
            # Cônjuge do locatário
            'locatario_conjuge_nome': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome completo do cônjuge'
            }),
            'locatario_conjuge_nacionalidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: Brasileira'
            }),
            'locatario_conjuge_profissao': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Profissão'
            }),
            'locatario_conjuge_rg': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '00.000.000-0'
            }),
            'locatario_conjuge_cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'
            }),
            
            # Imóvel
            'imovel_tipo': forms.Select(attrs={'class': 'form-select'}),
            'imovel_rua': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome da rua'
            }),
            'imovel_numero': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número'
            }),
            'imovel_bairro': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Bairro'
            }),
            'imovel_cidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Cidade'
            }),
            'imovel_estado': forms.Select(attrs={'class': 'form-select'}),
            'imovel_matricula': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número da matrícula (opcional)'
            }),
            'imovel_cartorio': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome do cartório (opcional)'
            }),
            'imovel_iptu': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número do IPTU (opcional)'
            }),
            'imovel_conta_agua': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número da conta de água (opcional)'
            }),
            'imovel_conta_luz': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número da conta de luz (opcional)'
            }),
            
            # Detalhes da locação
            'valor_aluguel': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': '0,00', 'step': '0.01'
            }),
            'valor_aluguel_extenso': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Valor por extenso'
            }),
            'forma_pagamento': forms.Select(attrs={'class': 'form-select'}),
            'dia_pagamento': forms.Select(attrs={'class': 'form-select'}),
            'conta_bancaria': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Dados da conta bancária'
            }),
            'data_inicio': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'data_termino': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            
            # Garantia
            'tipo_garantia': forms.Select(attrs={'class': 'form-select'}),
            'valor_caucao': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': '0,00', 'step': '0.01'
            }),
            
            # Fiador
            'fiador_nome': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome completo do fiador'
            }),
            'fiador_estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'fiador_nacionalidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex: Brasileira'
            }),
            'fiador_profissao': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Profissão'
            }),
            'fiador_rg': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '00.000.000-0'
            }),
            'fiador_cpf': forms.TextInput(attrs={
                'class': 'form-control cpf-mask', 'placeholder': '000.000.000-00'
            }),
            'fiador_rua': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome da rua'
            }),
            'fiador_numero': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Número'
            }),
            'fiador_bairro': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Bairro'
            }),
            'fiador_cidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Cidade'
            }),
            'fiador_estado': forms.Select(attrs={'class': 'form-select'}),
            
            # Seguro
            'seguro_nome_seguradora': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome da seguradora'
            }),
            'seguro_prazo': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Prazo do seguro'
            }),
            'seguro_valor': forms.NumberInput(attrs={
                'class': 'form-control', 'placeholder': '0,00', 'step': '0.01'
            }),
            
            # Observações
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4, 'placeholder': 'Observações adicionais'
            }),
        }
    
    def clean_proprietario_cpf(self):
        cpf = self.cleaned_data.get('proprietario_cpf')
        if cpf:
            # Remove formatação
            cpf = re.sub(r'[^\d]', '', cpf)
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_locatario_cpf(self):
        cpf = self.cleaned_data.get('locatario_cpf')
        if cpf:
            # Remove formatação
            cpf = re.sub(r'[^\d]', '', cpf)
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_fiador_cpf(self):
        cpf = self.cleaned_data.get('fiador_cpf')
        if cpf:
            # Remove formatação
            cpf = re.sub(r'[^\d]', '', cpf)
            if len(cpf) != 11:
                raise forms.ValidationError('CPF deve ter 11 dígitos.')
        return cpf
    
    def clean_valor_aluguel(self):
        valor = self.cleaned_data.get('valor_aluguel')
        if valor and valor <= 0:
            raise forms.ValidationError('O valor do aluguel deve ser maior que zero.')
        return valor
    
    def clean_data_termino(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        data_termino = self.cleaned_data.get('data_termino')
        
        if data_inicio and data_termino:
            if data_termino <= data_inicio:
                raise forms.ValidationError('A data de término deve ser posterior à data de início.')
        
        return data_termino
