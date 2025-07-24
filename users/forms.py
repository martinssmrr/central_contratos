from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """Formulário customizado para criação de usuário"""
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu nome',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu sobrenome',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True, 
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Customizar campos
        self.fields['username'].label = 'Nome de usuário'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Escolha um nome de usuário',
            'class': 'form-control'
        })
        
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Crie uma senha segura',
            'class': 'form-control'
        })
        
        self.fields['password2'].label = 'Confirmar senha'
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Digite novamente sua senha',
            'class': 'form-control'
        })
        
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2',
            HTML('<div class="form-check mb-3">'
                 '<input class="form-check-input" type="checkbox" id="terms" required>'
                 '<label class="form-check-label" for="terms">'
                 'Aceito os <a href="#" target="_blank">termos de uso</a> e <a href="#" target="_blank">política de privacidade</a>'
                 '</label></div>'),
            HTML('<div class="d-grid mb-3">'
                 '<button type="submit" class="btn btn-primary btn-lg fw-semibold">'
                 '<i class="fas fa-user-plus me-2"></i>Criar Minha Conta'
                 '</button>'
                 '</div>')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está sendo usado por outra conta.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Formulário customizado para login"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Customizar labels e placeholders
        self.fields['username'].label = 'E-mail ou usuário'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu e-mail ou nome de usuário',
            'class': 'form-control form-control-lg',
            'autofocus': True
        })
        
        self.fields['password'].label = 'Senha'
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Digite sua senha',
            'class': 'form-control form-control-lg'
        })
        
        self.helper.layout = Layout(
            'username',
            'password',
            HTML('<div class="form-check mb-3">'
                 '<input class="form-check-input" type="checkbox" id="remember" name="remember_me">'
                 '<label class="form-check-label text-muted" for="remember">Lembrar-me</label>'
                 '</div>'),
            HTML('<div class="d-grid mb-3">'
                 '<button type="submit" class="btn btn-primary btn-lg fw-semibold">'
                 '<i class="fas fa-sign-in-alt me-2"></i>Entrar na minha conta'
                 '</button>'
                 '</div>')
        )

class UserProfileForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(required=True, label='E-mail')
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'cpf_cnpj', 'birth_date', 'avatar']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'phone': 'Telefone',
            'address': 'Endereço',
            'cpf_cnpj': 'CPF/CNPJ',
            'birth_date': 'Data de Nascimento',
            'avatar': 'Foto do Perfil',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            HTML('<h4>Dados Pessoais</h4>'),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-8 mb-0'),
                Column('phone', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cpf_cnpj', css_class='form-group col-md-6 mb-0'),
                Column('birth_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address',
            'avatar',
            Submit('submit', 'Salvar Alterações', css_class='btn btn-primary btn-lg')
        )
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Atualizar dados do usuário
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile.save()
        
        return profile
