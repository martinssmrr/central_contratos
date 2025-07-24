from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.text import slugify
import json
from datetime import datetime, timedelta
from contracts.models import Contract, Payment, ContractType
from django.contrib.auth.models import User
from users.models import UserProfile

@staff_member_required
def dashboard_view(request):
    """Dashboard administrativo"""
    # Estatísticas gerais
    total_contracts = Contract.objects.count()
    paid_contracts = Contract.objects.filter(status='paid').count()
    pending_contracts = Contract.objects.filter(status='pending').count()
    total_revenue = Payment.objects.filter(status='approved').aggregate(
        total=Sum('amount'))['total'] or 0
    
    # Contratos por tipo
    contracts_by_type = Contract.objects.values(
        'contract_type__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Estatísticas do mês atual
    current_month = timezone.now().replace(day=1)
    month_contracts = Contract.objects.filter(created_at__gte=current_month).count()
    month_revenue = Payment.objects.filter(
        status='approved',
        payment_date__gte=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Contratos recentes
    recent_contracts = Contract.objects.select_related(
        'user', 'contract_type'
    ).order_by('-created_at')[:10]
    
    # Usuários cadastrados
    total_users = User.objects.count()
    month_users = User.objects.filter(date_joined__gte=current_month).count()
    
    context = {
        'total_contracts': total_contracts,
        'paid_contracts': paid_contracts,
        'pending_contracts': pending_contracts,
        'total_revenue': total_revenue,
        'contracts_by_type': contracts_by_type,
        'month_contracts': month_contracts,
        'month_revenue': month_revenue,
        'recent_contracts': recent_contracts,
        'total_users': total_users,
        'month_users': month_users,
    }
    
    return render(request, 'adminpanel/dashboard.html', context)

@staff_member_required
def contracts_report_view(request):
    """Relatório de contratos"""
    contracts = Contract.objects.select_related(
        'user', 'contract_type', 'payment'
    ).order_by('-created_at')
    
    # Filtros
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    
    if status_filter:
        contracts = contracts.filter(status=status_filter)
    
    if type_filter:
        contracts = contracts.filter(contract_type__slug=type_filter)
    
    # Dados para filtros
    contract_types = ContractType.objects.all()
    status_choices = Contract.STATUS_CHOICES
    
    context = {
        'contracts': contracts,
        'contract_types': contract_types,
        'status_choices': status_choices,
        'current_status': status_filter,
        'current_type': type_filter,
    }
    
    return render(request, 'adminpanel/contracts_report.html', context)

@staff_member_required
def payments_report_view(request):
    """Relatório de pagamentos"""
    payments = Payment.objects.select_related(
        'contract', 'contract__user'
    ).order_by('-created_at')
    
    # Filtros
    status_filter = request.GET.get('status')
    method_filter = request.GET.get('method')
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    if method_filter:
        payments = payments.filter(payment_method=method_filter)
    
    # Dados para filtros
    status_choices = Payment.STATUS_CHOICES
    method_choices = Payment.PAYMENT_METHODS
    
    context = {
        'payments': payments,
        'status_choices': status_choices,
        'method_choices': method_choices,
        'current_status': status_filter,
        'current_method': method_filter,
    }
    
    return render(request, 'adminpanel/payments_report.html', context)

@staff_member_required
def users_report_view(request):
    """Relatório de usuários"""
    users = User.objects.select_related('userprofile').order_by('-date_joined')
    
    # Estatísticas
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    verified_users = users.filter(userprofile__is_verified=True).count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'verified_users': verified_users,
    }
    
    return render(request, 'adminpanel/users_report.html', context)


@staff_member_required
def admin_panel_view(request):
    """Painel administrativo principal completo"""
    
    # Estatísticas básicas
    total_contracts = Contract.objects.count()
    paid_contracts = Contract.objects.filter(status='paid').count()
    pending_contracts = Contract.objects.filter(status='pending').count()
    total_revenue = Payment.objects.filter(status='approved').aggregate(
        total=Sum('amount'))['total'] or 0
    
    context = {
        'total_contracts': total_contracts,
        'paid_contracts': paid_contracts,
        'pending_contracts': pending_contracts,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'adminpanel/admin_panel.html', context)


@staff_member_required
def contracts_management_view(request):
    """Gestão completa de contratos criados pelos clientes"""
    
    # Filtros
    search = request.GET.get('search', '')
    contract_type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    
    # Query base
    contracts = Contract.objects.select_related(
        'user', 'contract_type', 'payment'
    ).order_by('-created_at')
    
    # Aplicar filtros
    if search:
        contracts = contracts.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search) |
            Q(contract_type__name__icontains=search)
        )
    
    if contract_type_filter:
        contracts = contracts.filter(contract_type__slug=contract_type_filter)
    
    if status_filter:
        contracts = contracts.filter(status=status_filter)
    
    if date_filter:
        if date_filter == 'today':
            contracts = contracts.filter(created_at__date=timezone.now().date())
        elif date_filter == 'week':
            week_ago = timezone.now() - timedelta(days=7)
            contracts = contracts.filter(created_at__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now() - timedelta(days=30)
            contracts = contracts.filter(created_at__gte=month_ago)
    
    # Paginação
    paginator = Paginator(contracts, 20)  # 20 contratos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para filtros
    contract_types = ContractType.objects.filter(is_active=True)
    status_choices = Contract.STATUS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'contracts': page_obj,
        'contract_types': contract_types,
        'status_choices': status_choices,
        'current_search': search,
        'current_type': contract_type_filter,
        'current_status': status_filter,
        'current_date': date_filter,
        'total_count': contracts.count(),
    }
    
    return render(request, 'adminpanel/contracts_management.html', context)


@staff_member_required
def contract_types_management_view(request):
    """Controle de preços e descrições dos contratos disponíveis"""
    
    contract_types = ContractType.objects.all().order_by('name')
    
    context = {
        'contract_types': contract_types,
    }
    
    return render(request, 'adminpanel/contract_types_management.html', context)


@staff_member_required
@require_http_methods(["POST"])
def update_contract_type_ajax(request):
    """Atualiza tipo de contrato via AJAX"""
    
    try:
        data = json.loads(request.body)
        contract_type_id = data.get('id')
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = data.get('price', '').strip()
        is_active = data.get('is_active', True)
        
        # Validações
        if not name:
            return JsonResponse({'success': False, 'message': 'Nome é obrigatório'})
        
        if not description:
            return JsonResponse({'success': False, 'message': 'Descrição é obrigatória'})
        
        try:
            price = float(price.replace(',', '.'))
            if price < 0:
                raise ValueError()
        except (ValueError, AttributeError):
            return JsonResponse({'success': False, 'message': 'Preço deve ser um valor válido'})
        
        # Atualizar no banco
        contract_type = get_object_or_404(ContractType, id=contract_type_id)
        contract_type.name = name
        contract_type.description = description
        contract_type.price = price
        contract_type.is_active = is_active
        contract_type.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Contrato "{name}" atualizado com sucesso!',
            'data': {
                'id': contract_type.id,
                'name': contract_type.name,
                'description': contract_type.description,
                'price': float(contract_type.price),
                'is_active': contract_type.is_active,
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'})


@staff_member_required
def contract_detail_admin_view(request, contract_id):
    """Visualização detalhada de um contrato para admin"""
    
    contract = get_object_or_404(
        Contract.objects.select_related('user', 'contract_type', 'payment'),
        id=contract_id
    )
    
    context = {
        'contract': contract,
    }
    
    return render(request, 'adminpanel/contract_detail_admin.html', context)


# ================== TESTE ==================

@staff_member_required
def test_view(request):
    """View de teste para verificar autenticação"""
    from django.utils import timezone
    context = {
        'now': timezone.now()
    }
    return render(request, 'adminpanel/test_page.html', context)

# ================== CRUD DE TIPOS DE CONTRATO ==================

@staff_member_required
def contract_types_crud_view(request):
    """Página CRUD completa para tipos de contrato"""
    
    # Busca e filtros
    search = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    
    contract_types = ContractType.objects.annotate(
        contracts_count=Count('contract')
    ).order_by('order', 'name')
    
    if search:
        contract_types = contract_types.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__icontains=search)
        )
    
    if category_filter:
        contract_types = contract_types.filter(category=category_filter)
        
    if status_filter == 'active':
        contract_types = contract_types.filter(is_active=True)
    elif status_filter == 'inactive':
        contract_types = contract_types.filter(is_active=False)
    
    # Paginação
    paginator = Paginator(contract_types, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categorias para filtro
    categories = ContractType.objects.values_list('category', flat=True).distinct().exclude(category='')
    
    # Estatísticas
    total_types = ContractType.objects.count()
    active_types = ContractType.objects.filter(is_active=True).count()
    total_contracts = Contract.objects.count()
    
    context = {
        'page_obj': page_obj,
        'contract_types': page_obj,
        'search': search,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'categories': categories,
        'total_count': contract_types.count(),
        'total_types': total_types,
        'active_types': active_types,
        'total_contracts': total_contracts,
    }
    
    return render(request, 'adminpanel/contract_types_crud.html', context)


@staff_member_required
def contract_type_create_view(request):
    """Criar novo tipo de contrato"""
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            price = request.POST.get('price', '0')
            category = request.POST.get('category', '').strip()
            icon = request.POST.get('icon', 'fas fa-file-contract').strip()
            color = request.POST.get('color', '#f4623a').strip()
            order = request.POST.get('order', '0')
            is_active = request.POST.get('is_active') == 'on'
            
            # Validações
            if not name:
                messages.error(request, 'Nome é obrigatório.')
                return redirect('adminpanel:contract_types_crud')
            
            # Verificar se já existe um tipo com mesmo nome
            if ContractType.objects.filter(name__iexact=name).exists():
                messages.error(request, f'Já existe um tipo de contrato com o nome "{name}".')
                return redirect('adminpanel:contract_types_crud')
                
            if not description:
                messages.error(request, 'Descrição é obrigatória.')
                return redirect('adminpanel:contract_types_crud')
            
            try:
                price = float(price.replace(',', '.'))
                if price < 0:
                    raise ValueError()
            except ValueError:
                messages.error(request, 'Preço deve ser um valor válido.')
                return redirect('adminpanel:contract_types_crud')
            
            try:
                order = int(order)
                if order < 0:
                    order = 0
            except ValueError:
                order = 0
            
            # Criar tipo de contrato
            contract_type = ContractType.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                icon=icon,
                color=color,
                order=order,
                is_active=is_active
            )
            
            # Upload de imagem se fornecida
            if 'image' in request.FILES:
                contract_type.image = request.FILES['image']
                contract_type.save()
            
            # Invalidar cache para atualizar front-end
            cache.delete('contract_types_active')
            cache.delete('featured_contracts')
            cache.delete('contract_types_by_category')
            
            messages.success(request, f'Tipo de contrato "{name}" criado com sucesso!')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar tipo de contrato: {str(e)}')
    
    return redirect('adminpanel:contract_types_crud')


@staff_member_required
def contract_type_edit_view(request, contract_type_id):
    """Editar tipo de contrato existente"""
    
    contract_type = get_object_or_404(ContractType, id=contract_type_id)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            base_price = request.POST.get('base_price', '0')
            category = request.POST.get('category', '').strip()
            is_active = request.POST.get('is_active') == 'on'
            
            # Novos campos visuais
            icon = request.POST.get('icon', '').strip()
            color = request.POST.get('color', '#f4623a')
            order = request.POST.get('order', '0')
            
            # Validações
            if not name:
                messages.error(request, 'Nome é obrigatório.')
                return redirect('adminpanel:contract_types_crud')
                
            # Verificar nome único
            if name != contract_type.name and ContractType.objects.filter(name__iexact=name).exists():
                messages.error(request, f'Já existe um tipo de contrato com o nome "{name}".')
                return redirect('adminpanel:contract_types_crud')
            
            try:
                base_price = float(base_price.replace(',', '.'))
                if base_price < 0:
                    raise ValueError()
            except ValueError:
                messages.error(request, 'Preço deve ser um valor válido.')
                return redirect('adminpanel:contract_types_crud')
            
            try:
                order = int(order) if order else 0
            except (ValueError, TypeError):
                order = 0
            
            # Atualizar tipo de contrato
            contract_type.name = name
            contract_type.description = description
            contract_type.base_price = base_price
            contract_type.category = category
            contract_type.is_active = is_active
            contract_type.icon = icon
            contract_type.color = color
            contract_type.order = order
            
            contract_type.save()
            
            # Invalidar cache para atualizar front-end
            cache_keys = [
                'contract_types_active',
                'featured_contracts',
                'contract_types_all',
                'contract_categories',
            ]
            
            for key in cache_keys:
                cache.delete(key)
            
            messages.success(request, f'Tipo de contrato "{name}" atualizado com sucesso!')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar tipo de contrato: {str(e)}')
    
    return redirect('adminpanel:contract_types_crud')


@staff_member_required
def contract_type_delete_view(request, contract_type_id):
    """Excluir tipo de contrato"""
    
    contract_type = get_object_or_404(ContractType, id=contract_type_id)
    
    # Verificar se há contratos usando este tipo
    contracts_count = Contract.objects.filter(contract_type=contract_type).count()
    
    if contracts_count > 0:
        messages.error(
            request, 
            f'Não é possível excluir "{contract_type.name}" pois há {contracts_count} contratos associados.'
        )
    else:
        try:
            name = contract_type.name
            contract_type.delete()
            
            # Invalidar cache para atualizar front-end
            cache.delete('contract_types_active')
            cache.delete('featured_contracts')
            
            messages.success(request, f'Tipo de contrato "{name}" excluído com sucesso!')
            
        except Exception as e:
            messages.error(request, f'Erro ao excluir tipo de contrato: {str(e)}')
    
    return redirect('adminpanel:contract_types_crud')


@csrf_exempt
@staff_member_required
def contract_type_quick_edit_ajax(request):
    """Edição rápida via AJAX - atualizada com cache invalidation"""
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método não permitido'})
    
    try:
        data = json.loads(request.body)
        contract_type_id = data.get('id')
        
        if not contract_type_id:
            return JsonResponse({'success': False, 'message': 'ID não fornecido'})
        
        contract_type = get_object_or_404(ContractType, id=contract_type_id)
        
        # Validações
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = data.get('price', '0')
        
        if not name:
            return JsonResponse({'success': False, 'message': 'Nome é obrigatório'})
        
        if not description:
            return JsonResponse({'success': False, 'message': 'Descrição é obrigatória'})
        
        try:
            price = float(str(price).replace(',', '.'))
            if price < 0:
                raise ValueError()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Preço deve ser um valor válido'})
        
        # Atualizar dados
        contract_type.name = name
        contract_type.description = description
        contract_type.price = price
        contract_type.is_active = data.get('is_active', True)
        
        if 'category' in data:
            contract_type.category = data.get('category', '').strip()
        
        contract_type.save()
        
        # Invalidar cache para sincronizar com front-end
        cache.delete('contract_types_active')
        cache.delete('featured_contracts')
        cache.delete(f'contract_type_{contract_type.slug}')
        
        return JsonResponse({
            'success': True, 
            'message': 'Tipo de contrato atualizado com sucesso!',
            'data': {
                'id': contract_type.id,
                'name': contract_type.name,
                'description': contract_type.description,
                'price': str(contract_type.price),
                'category': contract_type.category,
                'is_active': contract_type.is_active,
                'updated_at': contract_type.updated_at.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'})


@staff_member_required
def get_contract_type_ajax(request, contract_type_id):
    """Buscar dados de um tipo de contrato via AJAX"""
    
    try:
        contract_type = get_object_or_404(ContractType, id=contract_type_id)
        
        return JsonResponse({
            'success': True,
            'contract_type': {
                'id': contract_type.id,
                'name': contract_type.name,
                'description': contract_type.description,
                'price': str(contract_type.price),
                'category': contract_type.category or '',
                'is_active': contract_type.is_active,
                'slug': contract_type.slug,
                'created_at': contract_type.created_at.strftime('%d/%m/%Y %H:%M'),
                'updated_at': contract_type.updated_at.strftime('%d/%m/%Y %H:%M'),
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro: {str(e)}'})


@staff_member_required
def contract_type_data_view(request, contract_type_id):
    """Retorna dados do tipo de contrato em JSON para o modal de edição"""
    
    contract_type = get_object_or_404(ContractType, id=contract_type_id)
    
    data = {
        'id': contract_type.id,
        'name': contract_type.name,
        'description': contract_type.description or '',
        'base_price': float(contract_type.base_price),
        'category': contract_type.category or '',
        'is_active': contract_type.is_active,
        'icon': contract_type.icon or '',
        'color': contract_type.color or '#f4623a',
        'order': contract_type.order or 0,
        'created_at': contract_type.created_at.strftime('%d/%m/%Y'),
    }
    
    return JsonResponse(data)
