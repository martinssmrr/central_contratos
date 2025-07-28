from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
from contracts.models import ContractType
from decimal import Decimal
import json


class Cart:
    """Classe para gerenciar o carrinho de compras na sessão"""
    
    def __init__(self, request):
        """Inicializa o carrinho"""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Criar um carrinho vazio na sessão
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def add(self, contract_type, quantity=1, override_quantity=False):
        """Adiciona um contrato ao carrinho ou atualiza sua quantidade"""
        contract_id = str(contract_type.id)
        
        if contract_id not in self.cart:
            self.cart[contract_id] = {
                'quantity': 0,
                'price': str(contract_type.price)
            }
        
        if override_quantity:
            self.cart[contract_id]['quantity'] = quantity
        else:
            self.cart[contract_id]['quantity'] += quantity
            
        self.save()
    
    def save(self):
        """Marca a sessão como modificada para garantir que seja salva"""
        self.session.modified = True
    
    def remove(self, contract_type):
        """Remove um contrato do carrinho"""
        contract_id = str(contract_type.id)
        if contract_id in self.cart:
            del self.cart[contract_id]
            self.save()
    
    def clear(self):
        """Remove todos os itens do carrinho"""
        del self.session['cart']
        self.save()
    
    def get_total_price(self):
        """Calcula o preço total do carrinho"""
        return sum(Decimal(item['price']) * item['quantity'] 
                  for item in self.cart.values())
    
    def get_total_items(self):
        """Calcula o número total de itens no carrinho"""
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        """Itera sobre os itens do carrinho e obtém os contratos do banco de dados"""
        contract_ids = self.cart.keys()
        contracts = ContractType.objects.filter(id__in=contract_ids)
        cart = self.cart.copy()
        
        for contract in contracts:
            cart[str(contract.id)]['contract'] = contract
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """Conta todos os itens no carrinho"""
        return sum(item['quantity'] for item in self.cart.values())


def cart_view(request):
    """Exibe o carrinho de compras"""
    cart = Cart(request)
    
    context = {
        'cart': cart,
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
    }
    
    return render(request, 'contracts/cart.html', context)


@require_POST
def cart_add(request, contract_id):
    """Adiciona um contrato ao carrinho"""
    cart = Cart(request)
    contract = get_object_or_404(ContractType, id=contract_id, is_active=True)
    
    # Para contratos, geralmente é quantidade 1
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(contract_type=contract, quantity=quantity)
    
    messages.success(request, f'{contract.name} foi adicionado ao carrinho!')
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{contract.name} foi adicionado ao carrinho!',
            'cart_items': cart.get_total_items(),
            'cart_total': str(cart.get_total_price())
        })
    
    # Se não for AJAX, redireciona de volta ou para o carrinho
    return redirect(request.META.get('HTTP_REFERER', 'contracts:cart'))


@require_POST
def cart_remove(request, contract_id):
    """Remove um contrato do carrinho"""
    cart = Cart(request)
    contract = get_object_or_404(ContractType, id=contract_id)
    
    cart.remove(contract)
    
    messages.success(request, f'{contract.name} foi removido do carrinho!')
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{contract.name} foi removido do carrinho!',
            'cart_items': cart.get_total_items(),
            'cart_total': str(cart.get_total_price())
        })
    
    return redirect('contracts:cart')


@require_POST
def cart_clear(request):
    """Limpa todo o carrinho"""
    cart = Cart(request)
    cart.clear()
    
    messages.success(request, 'Carrinho foi limpo!')
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Carrinho foi limpo!',
            'cart_items': 0,
            'cart_total': '0.00'
        })
    
    return redirect('contracts:cart')


def get_cart_data(request):
    """Retorna dados do carrinho em formato JSON para AJAX"""
    cart = Cart(request)
    
    cart_items = []
    for item in cart:
        cart_items.append({
            'id': item['contract'].id,
            'name': item['contract'].name,
            'price': str(item['price']),
            'quantity': item['quantity'],
            'total_price': str(item['total_price'])
        })
    
    return JsonResponse({
        'items': cart_items,
        'total_items': cart.get_total_items(),
        'total_price': str(cart.get_total_price())
    })
