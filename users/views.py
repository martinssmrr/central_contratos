from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import UserProfile
from contracts.models import Contract

class CustomLoginView(LoginView):
    """View customizada para login"""
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Marcar que usuário acabou de fazer login para middleware"""
        response = super().form_valid(form)
        self.request.session['just_logged_in'] = True
        return response
    
    def get_success_url(self):
        try:
            user_profile = self.request.user.userprofile
            if user_profile.is_admin():
                return reverse_lazy('adminpanel:admin_panel')
        except:
            pass
        return reverse_lazy('users:profile')


class AdminLoginView(LoginView):
    """View de login exclusiva para administradores"""
    form_class = CustomAuthenticationForm
    template_name = 'users/admin_login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Verificar se usuário é admin antes de fazer login"""
        user = form.get_user()
        
        try:
            user_profile = user.userprofile
            if not user_profile.is_admin():
                messages.error(
                    self.request, 
                    'Esta área é restrita a usuários administrativos.'
                )
                return self.form_invalid(form)
        except:
            # Criar perfil se não existir e marcar como admin se for staff
            if user.is_staff or user.is_superuser:
                user_profile = UserProfile.objects.create(user=user, user_type='admin')
            else:
                messages.error(
                    self.request, 
                    'Esta área é restrita a usuários administrativos.'
                )
                return self.form_invalid(form)
        
        response = super().form_valid(form)
        self.request.session['just_logged_in'] = True
        return response
    
    def get_success_url(self):
        return reverse_lazy('adminpanel:admin_panel')

class CustomLogoutView(LogoutView):
    """View customizada para logout"""
    template_name = 'users/logout.html'
    next_page = 'core:home'
    http_method_names = ['get', 'post']  # Permite GET e POST
    
    def get(self, request, *args, **kwargs):
        """Mostra página de confirmação de logout"""
        if request.user.is_authenticated:
            # Usuário logado - mostra página de confirmação
            return render(request, self.template_name)
        else:
            # Usuário não logado - mostra página de sucesso
            return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        """Executa o logout"""
        if request.user.is_authenticated:
            messages.success(request, 'Logout realizado com sucesso!')
        return super().post(request, *args, **kwargs)

def register_view(request):
    """View para registro de usuário"""
    if request.user.is_authenticated:
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Você já pode fazer login.')
            
            # Fazer login automático
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user:
                login(request, user)
                return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    """View do perfil do usuário"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Estatísticas do usuário
    total_contracts = Contract.objects.filter(user=request.user).count()
    paid_contracts = Contract.objects.filter(user=request.user, status='paid').count()
    pending_contracts = Contract.objects.filter(user=request.user, status='pending').count()
    
    # Contratos recentes
    recent_contracts = Contract.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'total_contracts': total_contracts,
        'paid_contracts': paid_contracts,
        'pending_contracts': pending_contracts,
        'recent_contracts': recent_contracts,
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile_view(request):
    """View para edição do perfil"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})
