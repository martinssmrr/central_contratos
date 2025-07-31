from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from django.urls import reverse
# from weasyprint import HTML, CSS
# from weasyprint.text.fonts import FontConfiguration
import io
import os
from datetime import datetime

from .models import Category, ContractType, Contract, Payment, CompraVendaImovel, ContratoLocacaoResidencial
from .forms import (
    ContractForm, PrestacaoServicoForm, LocacaoForm, 
    CompraVendaForm, ConfissaoDividaForm, FreelancerForm, PaymentForm, CompraVendaImovelForm
)
# from .utils import generate_contract_pdf

def catalog_view(request):
    """Exibe o catálogo de contratos disponíveis"""
    # Obter parâmetro de categoria
    category_slug = request.GET.get('category')
    
    # Obter todas as categorias ativas
    categories = Category.objects.filter(is_active=True)
    
    # Filtrar contratos por categoria se especificada
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        contract_types = ContractType.objects.filter(
            category=category, 
            is_active=True
        )
        current_category = category
    else:
        contract_types = ContractType.objects.filter(is_active=True)
        current_category = None
    
    return render(request, 'contracts/catalog.html', {
        'contract_types': contract_types,
        'categories': categories,
        'current_category': current_category,
    })

def catalog_category_view(request, slug):
    """Exibe contratos de uma categoria específica"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    contract_types = ContractType.objects.filter(
        category=category, 
        is_active=True
    )
    categories = Category.objects.filter(is_active=True)
    
    return render(request, 'contracts/catalog.html', {
        'contract_types': contract_types,
        'categories': categories,
        'current_category': category,
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


# =====================================================================
# VIEWS DO MERCADO PAGO
# =====================================================================

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def create_payment_preference(request, contract_id):
    """Cria preferência de pagamento no Mercado Pago"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    
    try:
        # Obter ou criar pagamento
        payment, created = Payment.objects.get_or_create(
            contract=contract,
            defaults={
                'amount': contract.contract_type.price,
                'status': 'pending'
            }
        )
        
        from .mercado_pago import mercado_pago_service
        
        # Criar preferência
        result = mercado_pago_service.create_preference(payment, request)
        
        if result['success']:
            # Redirecionar para o checkout do Mercado Pago
            checkout_url = result['sandbox_init_point']  # Para produção: result['init_point']
            return redirect(checkout_url)
        else:
            messages.error(request, result['error'])
            return redirect('contracts:contract_detail', pk=contract.id)
            
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao criar preferência: {str(e)}")
        messages.error(request, 'Erro ao processar pagamento. Tente novamente.')
        return redirect('contracts:contract_detail', pk=contract.id)
        return redirect('contracts:contract_detail', pk=contract.id)


@login_required
def payment_success(request):
    """Página de sucesso do pagamento"""
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    contract_id = request.GET.get('contract_id')  # Para auto_return
    collection_id = request.GET.get('collection_id')
    
    context = {
        'payment_id': payment_id,
        'status': status,
        'external_reference': external_reference,
        'contract_id': contract_id,
        'collection_id': collection_id
    }
    
    # Priorizar contract_id do auto_return, depois external_reference
    target_contract_id = contract_id or external_reference
    
    # Buscar contrato se temos a referência
    if target_contract_id:
        try:
            contract = Contract.objects.get(id=int(target_contract_id))
            context['contract'] = contract
            
            # Se temos um pagamento aprovado, redirecionar automaticamente para download
            if status == 'approved' or (payment_id and collection_id):
                messages.success(request, f'Pagamento aprovado! Contrato {contract.contract_type.name} processado com sucesso.')
                return redirect('contracts:download_contract', pk=contract.id)
            
            # Atualizar status do pagamento se necessário
            if payment_id:
                from .mercado_pago import mercado_pago_service
                payment_info = mercado_pago_service.get_payment_info(payment_id)
                
                if payment_info['success']:
                    payment_data = payment_info['payment']
                    
                    # Atualizar ou criar pagamento
                    payment, created = Payment.objects.get_or_create(
                        contract=contract,
                        defaults={
                            'amount': contract.contract_type.price,
                            'status': 'pending'
                        }
                    )
                    
                    payment.update_from_mercadopago(payment_data)
                    context['payment'] = payment
                    
                    # Se pagamento foi aprovado, redirecionar para download
                    if payment.status == 'approved':
                        messages.success(request, f'Pagamento confirmado! Baixe seu contrato agora.')
                        return redirect('contracts:download_contract', pk=contract.id)
                    
        except (Contract.DoesNotExist, ValueError):
            pass
    
    return render(request, 'contracts/payment_success.html', context)


@login_required 
def payment_failure(request):
    """Página de falha no pagamento"""
    return render(request, 'contracts/payment_failure.html')


@login_required
def payment_pending(request):
    """Página de pagamento pendente"""
    contract_id = request.GET.get('contract_id')
    external_reference = request.GET.get('external_reference')
    
    context = {
        'contract_id': contract_id,
        'external_reference': external_reference
    }
    
    # Buscar contrato se temos a referência
    target_contract_id = contract_id or external_reference
    if target_contract_id:
        try:
            contract = Contract.objects.get(id=int(target_contract_id))
            context['contract'] = contract
        except (Contract.DoesNotExist, ValueError):
            pass
    
    return render(request, 'contracts/payment_pending.html', context)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def payment_webhook(request):
    """Webhook para notificações do Mercado Pago"""
    try:
        from .mercado_pago import mercado_pago_service
        
        result = mercado_pago_service.process_webhook(request)
        
        if result['success']:
            return HttpResponse("OK", status=200)
        else:
            return HttpResponse("Error", status=400)
            
    except Exception as e:
        logger.error(f"Erro no webhook: {str(e)}")
        return HttpResponse("Error", status=500)


@login_required
def download_contract(request, contract_id):
    """Download do contrato após pagamento aprovado"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    
    # Verificar se o pagamento foi aprovado
    try:
        payment = Payment.objects.get(contract=contract)
        if not payment.is_paid:
            messages.error(request, 'Pagamento não aprovado. Não é possível baixar o contrato.')
            return redirect('contracts:contract_detail', pk=contract.id)
    except Payment.DoesNotExist:
        messages.error(request, 'Pagamento não encontrado.')
        return redirect('contracts:contract_detail', pk=contract.id)
    
    # Aqui você implementaria a geração do PDF
    # Por enquanto, vamos mostrar uma página com as informações
    return render(request, 'contracts/download_contract.html', {
        'contract': contract,
        'payment': payment
    })


@login_required
def payment_status(request, contract_id):
    """API para verificar status do pagamento"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    
    try:
        payment = Payment.objects.get(contract=contract)
        
        return JsonResponse({
            'status': payment.status,
            'is_paid': payment.is_paid,
            'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
            'amount': str(payment.amount)
        })
        
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'not_found',
            'is_paid': False
        })

@login_required
def payment_status_check(request, contract_id):
    """View para verificar status do pagamento via AJAX"""
    try:
        contract = get_object_or_404(Contract, id=contract_id, user=request.user)
        payment = contract.payment
        
        return JsonResponse({
            'status': payment.status,
            'is_paid': payment.is_paid,
            'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
            'amount': str(payment.amount)
        })
        
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'not_found',
            'is_paid': False
        })

@login_required
def payment_page_view(request, contract_id):
    """Página de pagamento - exibe dados do contrato antes do pagamento"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    
    # Verificar se já existe pagamento para este contrato
    try:
        payment = Payment.objects.get(contract=contract)
        if payment.is_paid:
            # Se já foi pago, redirecionar para download
            return redirect('contracts:contract_detail', pk=contract.id)
    except Payment.DoesNotExist:
        # Se não existe pagamento, será criado na próxima etapa
        payment = None
    
    context = {
        'contract': contract,
        'payment': payment,
        'contract_type': contract.contract_type,
    }
    
    return render(request, 'contracts/payment.html', context)

@login_required
def process_payment_view(request, contract_id):
    """Processa o pagamento - cria preferência e redireciona para MP"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    
    try:
        # Obter ou criar pagamento
        payment, created = Payment.objects.get_or_create(
            contract=contract,
            defaults={
                'amount': contract.contract_type.price,
                'status': 'pending'
            }
        )
        
        # Verificar se já foi pago
        if payment.is_paid:
            messages.success(request, 'Este contrato já foi pago!')
            return redirect('contracts:contract_detail', pk=contract.id)
        
        from .mercado_pago import mercado_pago_service
        
        # Criar preferência no Mercado Pago
        result = mercado_pago_service.create_preference(payment, request)
        
        if result['success']:
            # Redirecionar para o checkout do Mercado Pago
            checkout_url = result['sandbox_init_point']  # Para produção: result['init_point']
            return redirect(checkout_url)
        else:
            messages.error(request, f"Erro ao processar pagamento: {result['error']}")
            return redirect('contracts:payment_page', contract_id=contract.id)
            
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao processar pagamento: {str(e)}")
        messages.error(request, 'Erro interno. Tente novamente em alguns instantes.')
        return redirect('contracts:payment_page', contract_id=contract.id)
