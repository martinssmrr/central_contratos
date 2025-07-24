from django import forms
from django.core.validators import EmailValidator
from django.core.mail import send_mail
from django.conf import settings


class ContactForm(forms.Form):
    """Formulário de contato"""
    
    SUBJECT_CHOICES = [
        ('general', 'Informações Gerais'),
        ('support', 'Suporte Técnico'),
        ('contracts', 'Dúvidas sobre Contratos'),
        ('billing', 'Questões de Pagamento'),
        ('partnership', 'Parcerias'),
        ('other', 'Outros'),
    ]
    
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo',
            'id': 'full_name',
        }),
        label='Nome Completo',
        help_text='Digite seu nome completo'
    )
    
    email = forms.EmailField(
        validators=[EmailValidator(message='Digite um e-mail válido')],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com',
            'id': 'email',
        }),
        label='E-mail',
        help_text='Utilizaremos este e-mail para responder sua mensagem'
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'subject',
        }),
        label='Assunto',
        help_text='Selecione o assunto que melhor descreve sua mensagem'
    )
    
    message = forms.CharField(
        min_length=10,
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua mensagem aqui...',
            'rows': 6,
            'id': 'message',
        }),
        label='Mensagem',
        help_text='Mínimo de 10 caracteres, máximo de 1000 caracteres'
    )
    
    def clean_full_name(self):
        """Validação customizada para nome completo"""
        full_name = self.cleaned_data.get('full_name')
        if full_name:
            # Verificar se tem pelo menos nome e sobrenome
            name_parts = full_name.strip().split()
            if len(name_parts) < 2:
                raise forms.ValidationError('Por favor, digite seu nome completo (nome e sobrenome)')
            
            # Verificar se contém apenas letras e espaços
            if not all(part.replace('-', '').replace("'", "").isalpha() for part in name_parts):
                raise forms.ValidationError('O nome deve conter apenas letras, espaços, hífens e apostrofes')
        
        return full_name
    
    def clean_message(self):
        """Validação customizada para mensagem"""
        message = self.cleaned_data.get('message')
        if message:
            # Verificar se não é apenas espaços
            if not message.strip():
                raise forms.ValidationError('A mensagem não pode estar vazia')
            
            # Verificar palavras mínimas
            words = message.strip().split()
            if len(words) < 3:
                raise forms.ValidationError('A mensagem deve ter pelo menos 3 palavras')
        
        return message
    
    def send_email(self):
        """Envia o e-mail de contato"""
        if self.is_valid():
            try:
                subject_dict = dict(self.SUBJECT_CHOICES)
                subject_text = subject_dict.get(self.cleaned_data['subject'], 'Outros')
                
                email_subject = f'[Central de Contratos] {subject_text} - {self.cleaned_data["full_name"]}'
                
                email_body = f"""
Nova mensagem de contato recebida:

Nome: {self.cleaned_data['full_name']}
E-mail: {self.cleaned_data['email']}
Assunto: {subject_text}

Mensagem:
{self.cleaned_data['message']}

---
Esta mensagem foi enviada através do formulário de contato do site Central de Contratos.
                """.strip()
                
                # Configurar e-mail de destino (pode ser configurado no settings.py)
                recipient_email = getattr(settings, 'CONTACT_EMAIL', 'contato@centraldecontratos.com')
                
                # Enviar e-mail
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )
                
                # E-mail de confirmação para o usuário
                confirmation_subject = 'Mensagem recebida - Central de Contratos'
                confirmation_body = f"""
Olá {self.cleaned_data['full_name']},

Recebemos sua mensagem e entraremos em contato em breve.

Resumo da sua mensagem:
Assunto: {subject_text}
Mensagem: {self.cleaned_data['message'][:100]}{'...' if len(self.cleaned_data['message']) > 100 else ''}

Obrigado pelo contato!

Equipe Central de Contratos
                """.strip()
                
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.cleaned_data['email']],
                    fail_silently=True,  # Não falhar se o e-mail de confirmação não for enviado
                )
                
                return True
                
            except Exception as e:
                # Log do erro (em produção, usar logging adequado)
                print(f"Erro ao enviar e-mail: {e}")
                return False
        
        return False
