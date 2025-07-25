from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse
# from weasyprint import HTML, CSS
# from weasyprint.text.fonts import FontConfiguration
import io
import os
from datetime import datetime

from .models import ContractType, Contract, Payment, CompraVendaImovel, ContratoLocacaoResidencial
from .forms import (
    ContractForm, PrestacaoServicoForm, LocacaoForm, 
    CompraVendaForm, ConfissaoDividaForm, FreelancerForm, PaymentForm, CompraVendaImovelForm
)
# from .utils import generate_contract_pdf

def catalog_view(request):
    """Exibe o catálogo de contratos disponíveis"""
    contract_types = ContractType.objects.filter(is_active=True)
    return render(request, 'contracts/catalog.html', {
        'contract_types': contract_types
    })

@login_required
def contract_form_view(request, slug):
    """Formulário para preenchimento dos dados do contrato"""
    contract_type = get_object_or_404(ContractType, slug=slug, is_active=True)
    
    # Selecionar o formulário correto baseado no tipo
    form_classes = {
        'prestacao_servico': PrestacaoServicoForm,
        'locacao_residencial': LocacaoForm,
        'locacao_comercial': LocacaoForm,
        'compra_venda': CompraVendaForm,
        'confissao_divida': ConfissaoDividaForm,
        'freelancer': FreelancerForm,
    }
    
    form_class = form_classes.get(slug, ContractForm)
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.user = request.user
            contract.contract_type = contract_type
            
            # Salvar dados específicos do tipo de contrato
            dados_especificos = {}
            if slug == 'prestacao_servico':
                dados_especificos = {
                    'servicos_detalhados': form.cleaned_data.get('servicos_detalhados'),
                    'local_prestacao': form.cleaned_data.get('local_prestacao'),
                }
            elif slug in ['locacao_residencial', 'locacao_comercial']:
                dados_especificos = {
                    'endereco_imovel': form.cleaned_data.get('endereco_imovel'),
                    'valor_caucao': str(form.cleaned_data.get('valor_caucao', 0)),
                    'dia_vencimento': form.cleaned_data.get('dia_vencimento'),
                }
            elif slug == 'compra_venda':
                dados_especificos = {
                    'descricao_bem': form.cleaned_data.get('descricao_bem'),
                    'local_entrega': form.cleaned_data.get('local_entrega'),
                    'prazo_entrega': form.cleaned_data.get('prazo_entrega'),
                }
            elif slug == 'confissao_divida':
                dados_especificos = {
                    'origem_divida': form.cleaned_data.get('origem_divida'),
                    'valor_juros': str(form.cleaned_data.get('valor_juros', 0)),
                    'data_vencimento': form.cleaned_data.get('data_vencimento').isoformat(),
                }
            elif slug == 'freelancer':
                dados_especificos = {
                    'projeto_detalhado': form.cleaned_data.get('projeto_detalhado'),
                    'prazo_entrega': form.cleaned_data.get('prazo_entrega'),
                    'direitos_autorais': form.cleaned_data.get('direitos_autorais'),
                }
            
            contract.dados_especificos = dados_especificos
            contract.save()
            
            # Criar registro de pagamento
            Payment.objects.create(
                contract=contract,
                amount=contract_type.price,
                payment_method='pending'
            )
            
            messages.success(request, 'Contrato criado com sucesso! Prossiga para o pagamento.')
            return redirect('contracts:payment', contract_id=contract.id)
    else:
        form = form_class()
    
    # Selecionar template específico baseado no tipo de contrato
    if slug == 'compra-venda':
        # Redirecionar para o formulário completo
        return redirect('contracts:compra_venda_completo')
    elif slug == 'locacao-residencial':
        # Redirecionar para o formulário de locação residencial
        return redirect('contracts:locacao_residencial')
    else:
        template_name = 'contracts/contract_form.html'
    
    return render(request, template_name, {
        'form': form,
        'contract_type': contract_type
    })

@login_required
def payment_view(request, contract_id):
    """Processamento do pagamento"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    payment = get_object_or_404(Payment, contract=contract)
    
    if payment.status == 'approved':
        return redirect('contracts:contract_detail', pk=contract.pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Simular processamento de pagamento
            payment_method = form.cleaned_data['payment_method']
            
            # Atualizar pagamento
            payment.payment_method = payment_method
            payment.status = 'approved'  # Simulando aprovação automática
            payment.payment_date = timezone.now()
            payment.transaction_id = f"TXN_{contract.id}_{int(timezone.now().timestamp())}"
            payment.save()
            
            # Atualizar status do contrato
            contract.status = 'paid'
            contract.save()
            
            # Gerar PDF - Implementar depois com WeasyPrint
            # pdf_content = generate_contract_pdf(contract)
            # if pdf_content:
            #     filename = f"contract_{contract.id}_{contract.contract_type.slug}.pdf"
            #     contract.pdf_file.save(filename, io.BytesIO(pdf_content), save=True)
            
            messages.success(request, 'Pagamento aprovado! Seu contrato está pronto para download.')
            return redirect('contracts:contract_detail', pk=contract.pk)
    else:
        form = PaymentForm()
    
    return render(request, 'contracts/payment.html', {
        'form': form,
        'contract': contract,
        'payment': payment
    })

@login_required
def contract_detail_view(request, pk):
    """Detalhes do contrato gerado"""
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    payment = get_object_or_404(Payment, contract=contract)
    
    return render(request, 'contracts/contract_detail.html', {
        'contract': contract,
        'payment': payment
    })

@login_required
def download_contract_view(request, pk):
    """Download do PDF do contrato"""
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    
    if contract.status != 'paid' or not contract.pdf_file:
        raise Http404("Contrato não encontrado ou não pago.")
    
    response = HttpResponse(contract.pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contract.id}.pdf"'
    return response

@login_required
@login_required
def user_contracts_view(request):
    """Lista os contratos do usuário"""
    contracts = Contract.objects.filter(user=request.user).select_related('contract_type', 'payment').order_by('-created_at')
    
    # Estatísticas para o dashboard
    total_contracts = contracts.count()
    paid_contracts = contracts.filter(status='paid').count()
    pending_contracts = contracts.filter(status='pending').count()
    cancelled_contracts = contracts.filter(status='cancelled').count()
    
    context = {
        'contracts': contracts,
        'total_contracts': total_contracts,
        'paid_contracts': paid_contracts,
        'pending_contracts': pending_contracts,
        'cancelled_contracts': cancelled_contracts,
    }
    
    return render(request, 'contracts/user_contracts.html', context)


@login_required
def compra_venda_imovel_view(request):
    """Formulário para contrato de compra e venda de imóvel"""
    if request.method == 'POST':
        form = CompraVendaImovelForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.user = request.user
            contrato.save()
            
            messages.success(request, 
                'Contrato de compra e venda criado com sucesso! '
                'Você pode visualizá-lo na área "Meus Contratos".'
            )
            return redirect('contracts:compra_venda_success', pk=contrato.pk)
        else:
            messages.error(request, 
                'Há erros no formulário. Por favor, verifique os campos destacados.'
            )
    else:
        form = CompraVendaImovelForm()
    
    return render(request, 'contracts/compra_venda_imovel_form.html', {
        'form': form,
        'title': 'Contrato de Compra e Venda de Imóvel'
    })


@login_required
def compra_venda_success_view(request, pk):
    """Página de sucesso após criação do contrato"""
    contrato = get_object_or_404(CompraVendaImovel, pk=pk, user=request.user)
    
    return render(request, 'contracts/compra_venda_success.html', {
        'contrato': contrato
    })


@login_required
def compra_venda_detail_view(request, pk):
    """Visualização detalhada do contrato de compra e venda"""
    contrato = get_object_or_404(CompraVendaImovel, pk=pk, user=request.user)
    
    return render(request, 'contracts/compra_venda_detail.html', {
        'contrato': contrato
    })


@login_required
def meus_contratos_compra_venda_view(request):
    """Lista dos contratos de compra e venda do usuário"""
    contratos = CompraVendaImovel.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'contracts/meus_contratos_compra_venda.html', {
        'contratos': contratos
    })


@login_required
def contrato_compra_venda_completo_view(request):
    """View para o formulário completo de compra e venda de imóvel"""
    from .forms import ContratoCompraVendaImovelForm
    from .models import ContratoCompraVendaImovel
    
    if request.method == 'POST':
        form = ContratoCompraVendaImovelForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.user = request.user
            
            # Processar datas das parcelas se for pagamento parcelado
            if contrato.forma_pagamento == 'parcelado':
                datas_parcelas = []
                parcela_count = 1
                
                while f'data_parcela_{parcela_count}' in request.POST:
                    data_parcela = request.POST.get(f'data_parcela_{parcela_count}')
                    if data_parcela:
                        datas_parcelas.append(data_parcela)
                    parcela_count += 1
                
                contrato.datas_parcelas = datas_parcelas
            
            contrato.save()
            
            messages.success(request, 
                'Contrato de compra e venda criado com sucesso! '
                'Você pode visualizá-lo na área "Meus Contratos".'
            )
            return redirect('contracts:compra_venda_detail_completo', pk=contrato.pk)
        else:
            messages.error(request, 
                'Há erros no formulário. Por favor, verifique os campos destacados.'
            )
    else:
        form = ContratoCompraVendaImovelForm()
    
    return render(request, 'contracts/compra_venda_completo_form.html', {
        'form': form,
        'title': 'Contrato de Compra e Venda de Imóvel Completo'
    })


@login_required
def compra_venda_detail_completo_view(request, pk):
    """Visualização detalhada do contrato completo"""
    from .models import ContratoCompraVendaImovel
    
    contrato = get_object_or_404(ContratoCompraVendaImovel, pk=pk, user=request.user)
    
    return render(request, 'contracts/compra_venda_detail_completo.html', {
        'contrato': contrato
    })


@login_required 
def compra_venda_success_completo_view(request, pk):
    """Página de sucesso após criação do contrato completo"""
    from .models import ContratoCompraVendaImovel
    
    contrato = get_object_or_404(ContratoCompraVendaImovel, pk=pk, user=request.user)
    
    return render(request, 'contracts/compra_venda_success_completo.html', {
        'contrato': contrato
    })


@login_required
def locacao_residencial_view(request):
    """View para o formulário completo de locação residencial"""
    from .forms import ContratoLocacaoResidencialForm
    from .models import ContratoLocacaoResidencial
    
    if request.method == 'POST':
        form = ContratoLocacaoResidencialForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.user = request.user
            contrato.save()
            
            messages.success(request, 'Contrato de locação residencial criado com sucesso!')
            return redirect('contracts:locacao_residencial_success', pk=contrato.pk)
    else:
        form = ContratoLocacaoResidencialForm()
    
    return render(request, 'contracts/locacao_residencial_form.html', {
        'form': form,
        'titulo': 'Contrato de Locação Residencial'
    })


@login_required
def locacao_residencial_detail_view(request, pk):
    """Visualização detalhada do contrato de locação residencial"""
    contrato = get_object_or_404(ContratoLocacaoResidencial, pk=pk, user=request.user)
    
    return render(request, 'contracts/locacao_residencial_detail.html', {
        'contrato': contrato
    })


@login_required
def locacao_residencial_success_view(request, pk):
    """Página de sucesso após criação do contrato de locação residencial"""
    contrato = get_object_or_404(ContratoLocacaoResidencial, pk=pk, user=request.user)
    
    return render(request, 'contracts/locacao_residencial_success.html', {
        'contrato': contrato
    })


@login_required
def meus_contratos_locacao_residencial_view(request):
    """Lista dos contratos de locação residencial do usuário"""
    contratos = ContratoLocacaoResidencial.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'contracts/meus_contratos_locacao_residencial.html', {
        'contratos': contratos
    })
