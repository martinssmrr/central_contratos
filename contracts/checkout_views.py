from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db import transaction
from contracts.models import ContractType, Contract, Payment
from contracts.cart_views import Cart
from django import forms


class CheckoutForm(forms.Form):
    """Formulário de checkout"""
    PAYMENT_METHOD_CHOICES = [
        ('pix', 'PIX'),
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('boleto', 'Boleto Bancário'),
    ]
    
    full_name = forms.CharField(
        max_length=200,
        label='Nome Completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo'
        })
    )
    
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        label='Método de Pagamento',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pré-preencher dados se usuário autenticado
        if user and user.is_authenticated:
            self.fields['full_name'].initial = user.get_full_name() or user.username
            self.fields['email'].initial = user.email


def checkout_view(request):
    """Página de checkout"""
    cart = Cart(request)
    
    # Verificar se o carrinho não está vazio
    if len(cart) == 0:
        messages.warning(request, 'Seu carrinho está vazio!')
        return redirect('contracts:cart')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        
        if form.is_valid():
            # Processar o checkout
            try:
                with transaction.atomic():
                    # Dados do formulário
                    full_name = form.cleaned_data['full_name']
                    email = form.cleaned_data['email']
                    payment_method = form.cleaned_data['payment_method']
                    
                    # Criar contratos para cada item do carrinho
                    created_contracts = []
                    
                    for item in cart:
                        contract_type = item['contract']
                        quantity = item['quantity']
                        
                        # Para cada quantidade (normalmente será 1 para contratos)
                        for _ in range(quantity):
                            # Criar contrato
                            contract = Contract.objects.create(
                                user=request.user if request.user.is_authenticated else None,
                                contract_type=contract_type,
                                status='pending',
                                # Dados básicos (serão preenchidos depois pelo usuário)
                                parte1_nome=full_name,
                                parte1_cpf_cnpj='',  # Será preenchido depois
                                parte1_endereco='',  # Será preenchido depois
                                parte2_nome='A definir',
                                parte2_cpf_cnpj='',
                                parte2_endereco='',
                                objeto_contrato=f'Contrato de {contract_type.name}',
                                valor=contract_type.price,
                                forma_pagamento=payment_method,
                                data_inicio=timezone.now().date(),
                                prazo_vigencia='12 meses'
                            )
                            
                            # Criar pagamento
                            payment = Payment.objects.create(
                                contract=contract,
                                status='pending',
                                payment_method=payment_method,
                                amount=contract_type.price
                            )
                            
                            created_contracts.append({
                                'contract': contract,
                                'payment': payment
                            })
                    
                    # Limpar carrinho
                    cart.clear()
                    
                    # Salvar dados na sessão para a página de sucesso
                    request.session['checkout_data'] = {
                        'contracts': [item['contract'].id for item in created_contracts],
                        'total_amount': str(sum(item['payment'].amount for item in created_contracts)),
                        'payment_method': payment_method,
                        'customer_name': full_name,
                        'customer_email': email
                    }
                    
                    messages.success(request, 'Pedido realizado com sucesso!')
                    return redirect('contracts:checkout_success')
                    
            except Exception as e:
                messages.error(request, f'Erro ao processar pedido: {str(e)}')
    else:
        form = CheckoutForm(user=request.user)
    
    context = {
        'form': form,
        'cart': cart,
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
    }
    
    return render(request, 'contracts/checkout.html', context)


def checkout_success_view(request):
    """Página de confirmação do pedido"""
    # Verificar se há dados do checkout na sessão
    checkout_data = request.session.get('checkout_data')
    
    if not checkout_data:
        messages.warning(request, 'Nenhum pedido encontrado.')
        return redirect('contracts:cart')
    
    # Buscar contratos criados
    contract_ids = checkout_data.get('contracts', [])
    contracts = Contract.objects.filter(id__in=contract_ids)
    
    context = {
        'checkout_data': checkout_data,
        'contracts': contracts,
        'total_amount': checkout_data.get('total_amount'),
        'payment_method': checkout_data.get('payment_method'),
        'customer_name': checkout_data.get('customer_name'),
        'customer_email': checkout_data.get('customer_email'),
    }
    
    # Limpar dados da sessão após exibir
    if 'checkout_data' in request.session:
        del request.session['checkout_data']
    
    return render(request, 'contracts/checkout_success.html', context)
