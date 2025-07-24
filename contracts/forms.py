from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Row, Column
from .models import Contract

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
