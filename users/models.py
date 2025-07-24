from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Perfil estendido do usuário"""
    USER_TYPES = [
        ('client', 'Cliente'),
        ('admin', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    user_type = models.CharField('Tipo de Usuário', max_length=10, choices=USER_TYPES, default='client')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    address = models.TextField('Endereço', blank=True)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, blank=True)
    birth_date = models.DateField('Data de Nascimento', blank=True, null=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField('Verificado', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.user_type == 'admin' or self.user.is_staff or self.user.is_superuser
    
    def is_client(self):
        """Verifica se o usuário é cliente"""
        return self.user_type == 'client' and not self.user.is_staff

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Cria perfil automaticamente quando um usuário é criado"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Salva o perfil quando o usuário é salvo"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
