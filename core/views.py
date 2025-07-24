from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from contracts.models import ContractType
from .forms import ContactForm

def home_view(request):
    """Página inicial do site"""
    # Usar cache para melhorar performance e sincronização
    featured_contracts = cache.get('featured_contracts')
    
    if featured_contracts is None:
        featured_contracts = list(ContractType.objects.filter(is_active=True)[:6])
        cache.set('featured_contracts', featured_contracts, 300)  # 5 minutos
    
    return render(request, 'core/home.html', {
        'featured_contracts': featured_contracts
    })

def about_view(request):
    """Página sobre nós"""
    return render(request, 'core/about.html')

def contact_view(request):
    """Página de contato"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Tentar enviar o e-mail
            if form.send_email():
                messages.success(
                    request, 
                    'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.'
                )
                return redirect('core:contact')
            else:
                messages.error(
                    request,
                    'Ocorreu um erro ao enviar sua mensagem. Tente novamente ou entre em contato diretamente.'
                )
        else:
            messages.error(
                request,
                'Por favor, corrija os erros abaixo e tente novamente.'
            )
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {
        'form': form
    })

def terms_view(request):
    """Termos de uso"""
    return render(request, 'core/terms.html')

def privacy_view(request):
    """Política de privacidade"""
    return render(request, 'core/privacy.html')
